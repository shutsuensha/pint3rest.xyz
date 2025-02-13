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
