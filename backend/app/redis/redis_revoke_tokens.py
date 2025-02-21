from redis import asyncio as aioredis
from app.config import settings
from app.logger import logger

redis_connection = None


async def init_redis_revoke_tokens():
    """Инициализация подключения к Redis для хранения отозванных токенов."""
    global redis_connection
    try:
        redis_connection = await aioredis.from_url(
            settings.REDIS_URL_REVOKE_TOKENS, decode_responses=True
        )
        logger.info("✅ Успешное подключение к Redis REVOKE TOKENS")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Redis REVOKE TOKENS: {e}")
        redis_connection = None  # Чтобы избежать использования сломанного соединения
    return redis_connection


async def close_redis_revoke_tokens():
    """Закрытие подключения к Redis для хранения отозванных токенов."""
    global redis_connection
    if redis_connection:
        try:
            await redis_connection.close()
            logger.info("🔴 Соединение с Redis REVOKE TOKENS закрыто")
        except Exception as e:
            logger.error(f"Ошибка при закрытии Redis для отозванных токенов: {e}")


async def revoke_token(token: str, ex: int) -> None:
    """Добавляет токен в блок-лист (ревокация)."""
    if not redis_connection:
        logger.error("Попытка добавить токен в блок-лист без инициализированного Redis.")
        raise Exception("Redis is not initialized. Call init_redis_revoke_tokens() first.")

    try:
        await redis_connection.set(name=token, value="1", ex=ex * 60)
    except Exception as e:
        logger.error(f"Ошибка при добавлении токена {token} в блок-лист: {e}")


async def is_token_revoked(token: str) -> bool:
    """Проверяет, есть ли токен в блок-листе."""
    if not redis_connection:
        logger.error("Попытка проверить токен без инициализированного Redis.")
        raise Exception("Redis is not initialized. Call init_redis_revoke_tokens() first.")

    try:
        revoked = await redis_connection.exists(token) > 0
        return revoked
    except Exception as e:
        logger.error(f"Ошибка при проверке токена {token} в блок-листе: {e}")
        return False