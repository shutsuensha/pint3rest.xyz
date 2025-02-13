from redis import asyncio as aioredis
from app.config import settings


redis_connection = None


async def init_redis_revoke_tokens():
    global redis_connection
    redis_connection = await aioredis.from_url(
        settings.REDIS_URL_REVOKE_TOKENS, decode_responses=True
    )
    return redis_connection


async def close_redis_revoke_tokens():
    await redis_connection.close()


async def revoke_token(token: str, ex: int) -> None:
    """Добавляет токен в блок-лист (ревокация)"""
    if not redis_connection:
        raise RuntimeError("Redis is not initialized. Call init_redis() first.")

    await redis_connection.set(name=token, value="1", ex=ex*60)


async def is_token_revoked(token: str) -> bool:
    """Проверяет, есть ли токен в блок-листе"""
    if not redis_connection:
        raise RuntimeError("Redis is not initialized. Call init_redis() first.")
    
    return await redis_connection.exists(token) > 0


