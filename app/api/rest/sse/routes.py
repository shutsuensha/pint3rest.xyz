import aiofiles
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import aiofiles
import os
from app.config import settings

from app.config import settings

from redis import asyncio as aioredis

import json
import uuid

from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import delete, desc, insert, or_, select, update

from fastapi.responses import FileResponse, StreamingResponse

from app.postgresql.database import async_session_maker

from app.api.rest.dependencies import db, filter, filter_with_value, user_id
from app.api.rest.tags.routes import get_all_tags
from app.api.rest.utils import extract_first_frame, get_primary_color, save_file
from app.config import settings
from app.postgresql.models import LikesOrm, PinsOrm, TagsOrm, UsersOrm, pins_tags, users_pins, users_view_pins, UsersRecommendationsPinsOrm, UpdatesOrm

from app.celery.tasks import make_user_recommendations

from app.api.rest.pins.schemas import PinOut


import asyncio

from typing import Dict

from redis import asyncio as aioredis

router = APIRouter(prefix="/sse", tags=["sse"])


templates = Jinja2Templates(directory="app/templates")


active_connections: Dict[int, asyncio.Queue] = {}


async def messages_event_stream(user_id: int):
    queue = asyncio.Queue()
    active_connections[user_id] = queue

    try:
        while True:
            message = await queue.get()  # Ждем нового сообщения для пользователя
            yield f"data: {json.dumps({'message': message})}\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        del active_connections[user_id]  # Удаляем соединение при закрытии


@router.get("/messages/stream/{user_id}")
async def stream(user_id: int):
    return StreamingResponse(messages_event_stream(user_id), media_type="text/event-stream")


@router.get("/video-stream")
async def video_stream(request: Request):
    file_path = settings.PATH_VIDEO_STREAM
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")

    # Если указан заголовок Range, обрабатываем запрос с диапазоном
    if range_header:
        try:
            # Пример заголовка: "bytes=0-"
            range_value = range_header.strip().lower().split('=')[1]
            start_str, end_str = range_value.split('-')
            start = int(start_str)
            end = int(end_str) if end_str else file_size - 1
        except Exception:
            raise HTTPException(status_code=400, detail="Неверный формат Range-заголовка")

        if start >= file_size or end >= file_size:
            raise HTTPException(status_code=416, detail="Диапазон вне границ файла")

        async def range_video_streamer():
            async with aiofiles.open(file_path, mode="rb") as video:
                # Перемещаем указатель на начало диапазона
                await video.seek(start)
                remaining = end - start + 1
                while remaining > 0:
                    # Проверяем, отключился ли клиент
                    if await request.is_disconnected():
                        print("Клиент отключился, прекращаем стриминг.")
                        break
                    # Читаем чанками по 1 МБ или оставшееся количество байт, если меньше
                    chunk_size = min(1024 * 1024, remaining)
                    chunk = await video.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
                    remaining -= len(chunk)

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": "video/mp4",
        }
        return StreamingResponse(range_video_streamer(), status_code=206, headers=headers)

    # Если заголовок Range не указан, отдаем весь файл
    else:
        async def full_video_streamer():
            async with aiofiles.open(file_path, mode="rb") as video:
                while True:
                    # Проверка отключения клиента
                    if await request.is_disconnected():
                        print("Клиент отключился, прекращаем стриминг.")
                        break
                    chunk = await video.read(1024 * 1024)  # Читаем чанками по 1 МБ
                    if not chunk:
                        break
                    yield chunk

        return StreamingResponse(full_video_streamer(), media_type="video/mp4")


@router.get("/", response_class=HTMLResponse)
async def ss_template(request: Request):
    return templates.TemplateResponse(
        request=request, name="sse.html", context={"API_DOMAIN": settings.API_DOMAIN}
    )


async def range_video_streamer(file_path: str, start: int, end: int, request: Request):
    async with aiofiles.open(file_path, mode="rb") as video:
        await video.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            # Проверяем, отключился ли клиент
            if await request.is_disconnected():
                print("Клиент отключился, прекращаем стриминг.")
                break
            
            chunk_size = min(1024 * 1024, remaining)
            chunk = await video.read(chunk_size)
            if not chunk:
                break
            yield chunk
            remaining -= len(chunk)


@router.get("/notauth/video-stream/{name}")
async def video_stream(name: str, request: Request):
    file_path = f"{settings.MEDIA_PATH}/stream/{name}"
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")
    
    if range_header is None:
        # Если заголовок Range отсутствует, возвращаем полный файл
        return StreamingResponse(aiofiles.open(file_path, mode="rb"), media_type="video/mp4")
    
    # Пример: "bytes=0-"
    try:
        range_value = range_header.strip().lower().split('=')[1]
        start_str, end_str = range_value.split('-')
        start = int(start_str)
        end = int(end_str) if end_str else file_size - 1
    except Exception:
        raise HTTPException(status_code=400, detail="Неверный формат Range-заголовка")
    
    if start >= file_size or end >= file_size:
        raise HTTPException(status_code=416, detail="Диапазон вне границ файла")
    
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
        "Content-Type": "video/mp4",
    }
    
    return StreamingResponse(
        range_video_streamer(file_path, start, end, request),
        status_code=206,
        headers=headers
    )


async def get_redis():
    return await aioredis.from_url(settings.REDIS_URL_CELERY_BROKER, decode_responses=True)


async def event_stream(user_id: int, make_recommendation: bool):
    redis = await get_redis()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"notifications:{user_id}")  # 🔥 Асинхронная подписка

    try:
        if make_recommendation:
            make_user_recommendations.delay(user_id)
        async for message in pubsub.listen():  # 🔥 Асинхронное получение сообщений
            if message["type"] == "message":
                yield f"data: {json.dumps({'message': message['data']})}\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe(f"notifications:{user_id}")  # Отключаемся от канала
        await pubsub.close()  # Закрываем соединение


@router.get("/updates/stream/{user_id}")
async def stream(user_id: int, db: db):
    result = await db.execute(select(UsersOrm).filter_by(id=user_id))
    user = result.scalars().first()
    make_recommendation = user.recommendation_created_at is None or user.recommendation_created_at.date() != datetime.now(timezone.utc).date()
    return StreamingResponse(event_stream(user_id, make_recommendation), media_type="text/event-stream")

