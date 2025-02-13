from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.users.routes import router as auth_router
from app.api.pins.routes import router as pin_router
from app.api.tags.routes import router as tag_router
from app.api.comments.routes import router as comment_router
from app.api.likes.routes import router as like_router
from app.api.subscription.routes import router as subscription_router
from app.api.messages.routes import router as messages_router
from app.api.chats.routes import router as chats_router

from .middlewares import register_middleware
from .websockets.chat import register_websocket

from app.redis.redis_app import init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield


app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(chats_router)
app.include_router(messages_router)
app.include_router(subscription_router)
app.include_router(pin_router)
app.include_router(tag_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(auth_router)


register_middleware(app)
register_websocket(app)


@app.get('/index/notauth/images/{id}')
async def get_image(id: int):
    if id <= 10:
        return FileResponse(f'app/media/carousel/{id}.jpg')
    else:
        return FileResponse(f'app/media/carousel/{id}.gif')