import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api.graphql.users.router import graphql_app
from app.api.rest.admin.routes import router as admin_router
from app.api.rest.boards.routes import router as boards_router
from app.api.rest.chats.routes import router as chats_router
from app.api.rest.comments.routes import router as comment_router
from app.api.rest.contact.routes import router as contact_router
from app.api.rest.likes.routes import router as like_router
from app.api.rest.messages.routes import router as messages_router
from app.api.rest.notauth.routes import router as notauth_router
from app.api.rest.pins.routes import router as pin_router
from app.api.rest.pins_cache.routes import router as pins_cache_router
from app.api.rest.recommendations.routes import router as recommendations_router
from app.api.rest.search.routes import router as search_router
from app.api.rest.sse.routes import router as sse_router
from app.api.rest.subscription.routes import router as subscription_router
from app.api.rest.tags.routes import router as tag_router
from app.api.rest.updates.routes import router as updates_router
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
        # await mongo.connect()
        await postgre_connect()
        # await mysql_connect()
        await init_httpx_client()
        yield
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации приложения: {e}")
    finally:
        await close_redis_revoke_tokens()
        await close_redis_cache()
        # await mongo.close()
        await close_httpx_client()


app = FastAPI(
    lifespan=lifespan,
    root_path="/api",
    title=title,
    description=description,
    version=version,
    license_info=license_info,
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

app.include_router(contact_router)
app.include_router(updates_router)
app.include_router(recommendations_router)
app.include_router(search_router)
app.include_router(admin_router)
app.include_router(boards_router)
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(os.path.dirname(__file__), "static/favicon.ico")
    return FileResponse(favicon_path)


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api" + app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="/favicon.ico",
        swagger_ui_parameters={
            "displayRequestDuration": True,  # Показывать время выполнения запросов
            "deepLinking": True,  # Позволяет ссылаться на конкретные секции API
            "defaultModelsExpandDepth": -1,  # Скрыть секцию моделей внизу
            "docExpansion": "none",  # Сворачивать все эндпоинты по умолчанию
            "filter": True,  # Включить поиск по API
            "showExtensions": True,  # Показывать дополнительные расширения API
            "showCommonExtensions": True,  # Показывать стандартные расширения API
            "persistAuthorization": True,  # Сохранять введенные токены авторизации при перезагрузке страницы
            "operationsSorter": "method",  # Сортировать эндпоинты по HTTP-методу (GET, POST и т.д.)
            "tryItOutEnabled": True,  # Разрешить редактирование запросов (Try it out)
        },
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/api" + app.openapi_url,
        title=app.title,
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        redoc_favicon_url="/favicon.ico",
    )
