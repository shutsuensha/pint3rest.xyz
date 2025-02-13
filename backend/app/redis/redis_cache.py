from redis import asyncio as aioredis
from app.config import settings


redis_connection = None


async def init_redis_cache():
    global redis_connection
    redis_connection = await aioredis.from_url(
        settings.REDIS_URL_CACHE
    )
    return redis_connection


async def close_redis_cache():
    await redis_connection.close()