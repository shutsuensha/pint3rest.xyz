from app.config import settings
from app.logger import logger
from redis import asyncio as aioredis

redis_connection = None


async def init_redis_limiter():
    """Инициализация подключения к Redis-Limiter."""
    global redis_connection
    try:
        redis_connection = await aioredis.from_url(settings.REDIS_URL_LIMITER)
        logger.info("✅ Успешное подключение к Redis Limiter")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Redis Limiter: {e}")
        redis_connection = None  # Чтобы избежать использования сломанного соединения
        raise e
    return redis_connection


async def close_redis_limiter():
    """Закрытие подключения к Redis-Limiter."""
    global redis_connection
    if redis_connection:
        try:
            await redis_connection.close()
            logger.info("🔴 Соединение с Redis Limiter закрыто")
        except Exception as e:
            logger.error(f"Ошибка при закрытии Redis-Limiter: {e}")
