from app.celery.celery_app import celery_instance
from app.mail.mail import mail, create_message
from asgiref.sync import async_to_sync  
from app.logger import logger
import shutil
from pathlib import Path
from PIL import Image
import io



@celery_instance.task
def send_email(recipients: list[str], subject: str, context: dict, template_name: str):
    try:
        message = create_message(recipients=recipients, subject=subject, context=context)
        async_to_sync(mail.send_message)(message, template_name=template_name)
    except Exception as e:
        logger.error(f"Ошибка при отправке email: {e}", exc_info=True)


@celery_instance.task
def save_file_celery(file_content: bytes, path: str):
    try:
        with open(path, "wb") as new_file:
            new_file.write(file_content)
        logger.info(f"img saved in: {path}")
        return True
    except Exception as e:
        logger.error(f"Ошибка сохранения файла {path}: {e}", exc_info=True)
        return False
    

@celery_instance.task
def save_file_celery_300x300(image_path: str, size=(300, 300)):
    try:
        with open(image_path, 'rb') as file:
            image = Image.open(file)
            image.load()  
        
        image.thumbnail(size)

        original_path = Path(image_path)
        new_filename = f"{original_path.stem}_{size[0]}x{size[1]}{original_path.suffix}"
        new_path = original_path.with_name(new_filename)

        image.save(new_path, format=image.format)

        logger.info(f"Image resized and saved in: {new_path}")
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {e}", exc_info=True)
