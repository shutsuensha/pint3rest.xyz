import aioboto3
from app.config import settings
from app.logger import logger

s3_client = None

async def init_s3_client():
    global s3_client
    try:
        session = aioboto3.Session()

        async with session.client(
            "s3",
            endpoint_url="https://storage.yandexcloud.net",
            aws_access_key_id=settings.YANDEX_STORAGE_KEY,
            aws_secret_access_key=settings.YANDEX_STORAGE_SECRET_KEY,
            region_name="ru-central1"
        ) as client:
            s3_client = client
            logger.info("✅ Успешное подключение к Yandex Object Storage")

    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Yandex Object Storage: {str(e)}")
        raise e
    

def get_s3_client():
    return s3_client
    

async def close_s3_client():
    global s3_client
    if s3_client:
        await s3_client.close()
        logger.info("🔴 Соединение с Yandex Object Storage закрыто")
