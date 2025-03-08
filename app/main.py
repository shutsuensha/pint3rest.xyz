from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api.graphql.users.router import graphql_app
from app.api.rest.chats.routes import router as chats_router
from app.api.rest.comments.routes import router as comment_router
from app.api.rest.likes.routes import router as like_router
from app.api.rest.messages.routes import router as messages_router
from app.api.rest.notauth.routes import router as notauth_router
from app.api.rest.pins.routes import router as pin_router
from app.api.rest.pins_cache.routes import router as pins_cache_router
from app.api.rest.sse.routes import router as sse_router
from app.api.rest.subscription.routes import router as subscription_router
from app.api.rest.tags.routes import router as tag_router
from app.api.rest.users.routes import router as users_router
from app.api.rest.users_celery.routes import router as users_celery_router
from app.api.rest.users_google_auth.routes import router as users_google_auth_router
from app.api.rest.users_httpx.routes import router as users_httpx_router
from app.api.rest.users_mongodb.routes import router as users_mongodb_router
from app.api.rest.users_mysql.routes import router as users_mysql_router
from app.api.rest.users_yandex_s3.routes import router as users_yandex_s3_router
from app.exceptions import register_exception_handlers
from app.httpx.app import close_httpx_client, init_httpx_client
from app.logger import logger
from app.mongodb.database import mongo
from app.mysql.test_connection import connect as mysql_connect
from app.postgresql.test_connection import connect as postgre_connect
from app.redis.redis_cache import close_redis_cache, init_redis_cache
from app.redis.redis_revoke_tokens import (
    close_redis_revoke_tokens,
    init_redis_revoke_tokens,
)

from .api_metadata import description, license_info, tags_metadata, title, version
from .middlewares import register_middleware
from .websockets.chat import register_websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_redis_revoke_tokens()
        redis_cache = await init_redis_cache()
        FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
        await mongo.connect()
        await postgre_connect()
        await mysql_connect()
        await init_httpx_client()
        yield
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации приложения: {e}")
    finally:
        await close_redis_revoke_tokens()
        await close_redis_cache()
        await mongo.close()
        await close_httpx_client()


app = FastAPI(
    lifespan=lifespan,
    root_path="/api",
    title=title,
    description=description,
    version=version,
    license_info=license_info,
    openapi_tags=tags_metadata,
)


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
app.include_router(users_google_auth_router)
app.include_router(users_yandex_s3_router)
app.include_router(users_httpx_router)
app.include_router(users_mysql_router)
app.include_router(users_mongodb_router)
app.include_router(users_celery_router)
app.include_router(notauth_router)
app.include_router(sse_router)


register_middleware(app)
register_websocket(app)
register_exception_handlers(app)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
