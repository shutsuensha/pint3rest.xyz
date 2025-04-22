import random
from datetime import datetime, timezone
from pathlib import Path

from asgiref.sync import async_to_sync
from PIL import Image
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

import redis
from app.api.rest.updates.schemas import UpdateResponse
from app.celery.celery_app import celery_instance
from app.config import settings
from app.logger import logger
from app.mail.mail import create_message, mail
from app.postgresql.database import get_sync_db
from app.postgresql.models import (
    CommentsOrm,
    PinsOrm,
    SubsrciptionsOrm,
    UpdatesOrm,
    UsersOrm,
    UsersRecommendationsPinsOrm,
    pins_tags,
    users_view_pins,
)

redis_client = redis.Redis.from_url(settings.REDIS_URL_CELERY_BROKER, decode_responses=True)


@celery_instance.task
def send_email_adds():
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        logger.error(f"Error getting sync db session: {e}", exc_info=True)
        raise e

    try:
        users = db.scalars(select(UsersOrm).where(UsersOrm.verified == True)).all()

        unique_emails = list({user.email for user in users if user.email})

        context = {"home_link": settings.FRONTEND_DOMAIN}
        emails = unique_emails
        subject = "Pinterest - create your ideas!"

        send_email(emails, subject, context, "mail_adds.html")
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def send_email(
    recipients: list[str],
    subject: str,
    context: dict,
    template_name: str,
    attachment: str | None = None,
):
    try:
        message = create_message(
            recipients=recipients, subject=subject, context=context, attachment=attachment
        )
        async_to_sync(mail.send_message)(message, template_name=template_name)
    except Exception as e:
        logger.error(f"Ошибка при отправке email: {e}", exc_info=True)
        raise e


@celery_instance.task
def save_file_celery_and_crop_300x300(file_content: bytes, path: str, user_id: int):
    try:
        with open(path, "wb") as new_file:
            new_file.write(file_content)
        logger.info(f"img saved in: {path}")
    except Exception as e:
        logger.error(f"Ошибка сохранения картинки {path}: {e}", exc_info=True)
        raise e

    image_path = path
    size = (300, 300)

    try:
        with open(image_path, "rb") as file:
            image = Image.open(file)
            image.load()

        image.thumbnail(size)

        original_path = Path(image_path)
        new_filename = f"{original_path.stem}_{size[0]}x{size[1]}{original_path.suffix}"
        new_path = original_path.with_name(new_filename)

        image.save(new_path, format=image.format)

        logger.info(f"Image resized and saved in: {new_path}")
    except Exception as e:
        logger.error(f"Error processing crop 300x300 {image_path}: {e}", exc_info=True)
        raise e

    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        logger.error(f"Error getting sync db session: {e}", exc_info=True)
        raise e

    try:
        db.execute(
            update(UsersOrm).where(UsersOrm.id == user_id).values(image=path).returning(UsersOrm)
        )
        db.commit()
        logger.info(f"User {user_id} image path updated in database")
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e

    return {"image saved path": path, "image saved 300x300 path": str(new_path)}


@celery_instance.task
def user_view_pin(user_id: int, pin_id: int):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        existing_link = db.execute(
            select(users_view_pins).where(
                (users_view_pins.c.user_id == user_id) & (users_view_pins.c.pin_id == pin_id)
            )
        )
        if not existing_link.scalar():
            stmt = insert(users_view_pins).values(user_id=user_id, pin_id=pin_id)
            db.execute(stmt)
            db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_user_recommendations(user_id: int):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        result = db.execute(select(users_view_pins).where(users_view_pins.c.user_id == user_id))
        pins_viewed = result.fetchall()

        if not pins_viewed:
            return

        result_pins = []
        for el in pins_viewed:
            result = db.execute(select(pins_tags).where(pins_tags.c.pin_id == el[1]))
            rows = result.all()

            pins = {}

            for row in rows:
                tag_id = row[1]

                new_result = db.execute(select(pins_tags).where(pins_tags.c.tag_id == tag_id))
                new_rows = new_result.all()

                for new_row in new_rows:
                    pin_id = new_row[0]
                    pin_db = db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
                    if pin_db.id not in pins and el[1] != pin_db.id:
                        pins[pin_db.id] = pin_db

            result_pins.extend([pin.id for pin in pins.values()])

        unique_pins = list(set(result_pins))

        if not unique_pins:
            return

        messages = [
            "Excellent taste!",
            "These ideas are in your style!",
            "You'll like these pins.",
            "This matches your vibe.",
            "Based on your preferences.",
        ]

        new_update = UpdatesOrm(
            user_update_to_id=user_id,
            content=random.choice(messages),
            update_type="recommendations",
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        for id in unique_pins:
            stmt = insert(UsersRecommendationsPinsOrm).values(
                user_id=user_id, pin_id=id, update_id=new_update.id
            )
            db.execute(stmt)
        db.commit()

        stmt = delete(users_view_pins).where(users_view_pins.c.user_id == user_id)
        db.execute(stmt)
        db.commit()

        user = db.get(UsersOrm, user_id)
        user.recommendation_created_at = datetime.now(timezone.utc)
        db.commit()

        update_data = UpdateResponse(
            id=new_update.id,
            content=new_update.content,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
        )

        redis_client.publish(f"notifications:{user_id}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_follow(user_update_to: int, user_follow: int):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        new_update = UpdatesOrm(
            user_update_to_id=user_update_to, update_type="follow", user_id=user_follow
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        update_data = UpdateResponse(
            id=new_update.id,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
            user_id=new_update.user_id,
        )

        redis_client.publish(f"notifications:{user_update_to}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_like_pin(user_update_to: int, user_liked: int, pin_id: int):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        new_update = UpdatesOrm(
            user_update_to_id=user_update_to,
            update_type="like_pin",
            user_id=user_liked,
            pin_id=pin_id,
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        update_data = UpdateResponse(
            id=new_update.id,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
            user_id=new_update.user_id,
            pin_id=new_update.pin_id,
        )

        redis_client.publish(f"notifications:{user_update_to}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_save_pin(user_update_to: int, user_saved: int, pin_id: int, where_to_save: str):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        new_update = UpdatesOrm(
            user_update_to_id=user_update_to,
            update_type="save_pin",
            content=where_to_save,
            user_id=user_saved,
            pin_id=pin_id,
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        update_data = UpdateResponse(
            id=new_update.id,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
            content=new_update.content,
            user_id=new_update.user_id,
            pin_id=new_update.pin_id,
        )

        redis_client.publish(f"notifications:{user_update_to}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_comment_pin(user_update_to: int, user_commented: int, pin_id: int, comment_id: int):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        new_update = UpdatesOrm(
            user_update_to_id=user_update_to,
            update_type="comment_pin",
            user_id=user_commented,
            pin_id=pin_id,
            comment_id=comment_id,
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        update_data = UpdateResponse(
            id=new_update.id,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
            user_id=new_update.user_id,
            pin_id=new_update.pin_id,
            comment_id=new_update.comment_id,
        )

        redis_client.publish(f"notifications:{user_update_to}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_like_comment(user_update_to: int, user_liked: int, comment_id: int, pin_id):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        new_update = UpdatesOrm(
            user_update_to_id=user_update_to,
            update_type="like_comment",
            user_id=user_liked,
            pin_id=pin_id,
            comment_id=comment_id,
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        update_data = UpdateResponse(
            id=new_update.id,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
            user_id=new_update.user_id,
            pin_id=new_update.pin_id,
            comment_id=new_update.comment_id,
        )

        redis_client.publish(f"notifications:{user_update_to}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_reply_comment(
    user_update_to: int, user_commented: int, pin_id: int, comment_id: int, reply_id
):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        new_update = UpdatesOrm(
            user_update_to_id=user_update_to,
            update_type="reply_comment",
            user_id=user_commented,
            pin_id=pin_id,
            comment_id=comment_id,
            reply_id=reply_id,
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        update_data = UpdateResponse(
            id=new_update.id,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
            user_id=new_update.user_id,
            pin_id=new_update.pin_id,
            comment_id=new_update.comment_id,
            reply_id=new_update.reply_id,
        )

        redis_client.publish(f"notifications:{user_update_to}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_like_reply(user_update_to: int, user_liked: int, reply_id: int, comment_id: int):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        comment = db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
        new_update = UpdatesOrm(
            user_update_to_id=user_update_to,
            update_type="like_reply",
            user_id=user_liked,
            pin_id=comment.pin_id,
            comment_id=comment_id,
            reply_id=reply_id,
        )
        db.add(new_update)
        db.commit()
        db.refresh(new_update)

        update_data = UpdateResponse(
            id=new_update.id,
            created_at=new_update.created_at,
            is_read=new_update.is_read,
            update_type=new_update.update_type,
            user_id=new_update.user_id,
            pin_id=new_update.pin_id,
            comment_id=new_update.comment_id,
            reply_id=new_update.reply_id,
        )

        redis_client.publish(f"notifications:{user_update_to}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e


@celery_instance.task
def make_update_pin_created_for_followers(user_id: int, pin_id: int):
    try:
        db = next(get_sync_db())
    except SQLAlchemyError as e:
        raise e

    try:
        stmt = select(SubsrciptionsOrm).where(SubsrciptionsOrm.following_id == user_id)
        subscriptions = db.scalars(stmt).all()
        for subsciber in subscriptions:
            new_update = UpdatesOrm(
                user_update_to_id=subsciber.follower_id,
                update_type="pin_created_for_followers",
                user_id=user_id,
                pin_id=pin_id,
            )
            db.add(new_update)
            db.commit()
            db.refresh(new_update)

            update_data = UpdateResponse(
                id=new_update.id,
                created_at=new_update.created_at,
                is_read=new_update.is_read,
                update_type=new_update.update_type,
                user_id=new_update.user_id,
                pin_id=new_update.pin_id,
            )

            redis_client.publish(f"notifications:{subsciber.follower_id}", update_data.json())
    except Exception as e:
        db.rollback()
        logger.error(f"Celery error using sync db connection: {e}", exc_info=True)
        raise e
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing db session: {e}", exc_info=True)
            raise e
