from redis import asyncio as aioredis
from app.config import settings
from app.logger import logger

redis_connection = None


async def init_redis_cache():
    """Инициализация подключения к Redis-кэшу."""
    global redis_connection
    try:
        redis_connection = await aioredis.from_url(settings.REDIS_URL_CACHE)
        logger.info(f"{settings.REDIS_URL_CACHE} Redis cache connected.")
    except Exception as e:
        logger.error(f"Ошибка при подключении к Redis-кэшу: {e}")
        redis_connection = None  # Чтобы избежать использования сломанного соединения
    return redis_connection


async def close_redis_cache():
    """Закрытие подключения к Redis-кэшу."""
    global redis_connection
    if redis_connection:
        try:
            await redis_connection.close()
            logger.info(f"{settings.REDIS_URL_CACHE} Redis cache closed.")
        except Exception as e:
            logger.error(f"Ошибка при закрытии Redis-кэша: {e}")
