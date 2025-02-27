from fastapi import Response
from fastapi_cache import FastAPICache


def pins_cache_key(func, *args, **kwargs):
    filter = kwargs['kwargs']['filter']
    offset = filter.offset
    limit = filter.limit
    return f"pins:offset={offset}:limit={limit}"


async def clear_all_pins_cache():
    redis_backend = FastAPICache.get_backend()
    keys = await redis_backend.redis.keys("pins:*") 
    if keys:
        await redis_backend.redis.delete(*keys)


def disable_client_cache(response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"