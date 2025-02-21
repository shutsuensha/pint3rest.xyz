from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.rest.users.routes import router as users_router
from app.api.rest.pins.routes import router as pin_router
from app.api.rest.tags.routes import router as tag_router
from app.api.rest.comments.routes import router as comment_router
from app.api.rest.likes.routes import router as like_router
from app.api.rest.subscription.routes import router as subscription_router
from app.api.rest.messages.routes import router as messages_router
from app.api.rest.chats.routes import router as chats_router
from app.api.rest.notauth.routes import router as notauth_router
from app.api.rest.users_celery.routes import router as users_celery_router
from app.api.rest.users_mongodb.routes import router as users_mongodb_router
from app.api.rest.pins_cache.routes import router as pins_cache_router


from .middlewares import register_middleware
from .websockets.chat import register_websocket

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.redis.redis_revoke_tokens import (
    init_redis_revoke_tokens,
    close_redis_revoke_tokens,
)
from app.redis.redis_cache import init_redis_cache, close_redis_cache

from app.logger import logger

from app.exceptions import register_exception_handlers

from app.api.graphql.users.router import graphql_app

from app.mongodb.database import mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_redis_revoke_tokens()
        redis_cache = await init_redis_cache()
        FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
        logger.info("✅ Успешное подключение к FastAPICache")
        await mongo.connect()
        yield
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации приложения: {e}")
    finally:
        await close_redis_revoke_tokens()
        await close_redis_cache()
        await mongo.close()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

app.include_router(chats_router)
app.include_router(messages_router)
app.include_router(subscription_router)
app.include_router(pin_router)
app.include_router(pins_cache_router)
app.include_router(tag_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(users_router)
app.include_router(users_mongodb_router)
app.include_router(users_celery_router)
app.include_router(notauth_router)


register_middleware(app)
register_websocket(app)
register_exception_handlers(app)