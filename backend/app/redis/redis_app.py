from redis import asyncio as aioredis
from app.config import settings


redis_connection = None


async def init_redis():
    global redis_connection
    redis_connection = await aioredis.from_url(
        settings.REDIS_URL, decode_responses=True
    )


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
