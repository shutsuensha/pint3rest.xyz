import json
import uuid

from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import delete, desc, insert, or_, select, update

from fastapi.responses import FileResponse, StreamingResponse

from app.postgresql.database import async_session_maker

from app.api.rest.dependencies import db, filter, filter_with_value, user_id
from app.api.rest.tags.routes import get_all_tags
from app.api.rest.utils import extract_first_frame, get_primary_color, save_file
from app.config import settings
from app.postgresql.models import LikesOrm, PinsOrm, TagsOrm, UsersOrm, pins_tags, users_pins, users_view_pins, UsersRecommendationsPinsOrm, UpdatesOrm

from app.celery.tasks import make_user_recommendations

from app.api.rest.pins.schemas import PinOut

from .schemas import UpdateResponse

import asyncio

from typing import Dict

from redis import asyncio as aioredis

router = APIRouter(prefix="/updates", tags=["updates"])


async def get_redis():
    return await aioredis.from_url(settings.REDIS_URL_CELERY_BROKER, decode_responses=True)


async def event_stream(user_id: int, make_recommendation: bool):
    redis = await get_redis()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"notifications:{user_id}")  # 🔥 Асинхронная подписка

    try:
        if make_recommendation:
            make_user_recommendations.delay(user_id)
        async for message in pubsub.listen():  # 🔥 Асинхронное получение сообщений
            if message["type"] == "message":
                yield f"data: {json.dumps({'message': message['data']})}\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe(f"notifications:{user_id}")  # Отключаемся от канала
        await pubsub.close()  # Закрываем соединение


@router.get("/stream/{user_id}")
async def stream(user_id: int, db: db):
    result = await db.execute(select(UsersOrm).filter_by(id=user_id))
    user = result.scalars().first()
    make_recommendation = user.recommendation_created_at is None or user.recommendation_created_at.date() != datetime.now(timezone.utc).date()
    return StreamingResponse(event_stream(user_id, True), media_type="text/event-stream")


@router.get("/count")
async def get_updates_count(user_id: user_id, db: db):
    result = await db.execute(
        select(UpdatesOrm)
        .where(UpdatesOrm.user_update_to_id == user_id, UpdatesOrm.is_read == False)
    )
    return len(result.fetchall())


@router.get("/", response_model=list[UpdateResponse])
async def get_updates(user_id: user_id, db: db, filter: filter):
    result = await db.execute(
        select(UpdatesOrm)
        .where(UpdatesOrm.user_update_to_id == user_id)
        .order_by(UpdatesOrm.created_at.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )
    return result.scalars().all()


@router.get('/{update_id}', response_model=UpdateResponse)
async def get_update_by_id(update_id: int, user_id: user_id, db: db):
    stmt = select(UpdatesOrm).filter(UpdatesOrm.id == update_id)
    result = await db.execute(stmt)
    update = result.scalars().first()
    return update



@router.put("/read/{update_id}")
async def mark_update_as_read(update_id: int, db: db):
    result = await db.execute(select(UpdatesOrm).where(UpdatesOrm.id == update_id))
    update = result.scalars().first()

    if not update:
        raise HTTPException(status_code=404, detail="Update not found")

    update.is_read = True
    await db.commit()


