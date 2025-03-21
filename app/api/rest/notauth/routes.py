from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, StreamingResponse
import aiofiles
from app.config import settings
import asyncio

router = APIRouter(prefix="/notauth", tags=["notauth"])


@router.get("/images/{id}")
async def get_image(id: int):
    path = f"{settings.MEDIA_PATH}notauth/{id}.jpg"
    return FileResponse(path)



async def video_streamer(name: str, request: Request):
    file_path = f"{settings.MEDIA_PATH}/stream/{name}"
    try:
        async with aiofiles.open(file_path, mode="rb") as video:
            while chunk := await video.read(1024 * 1024):  # Читаем чанками по 1MB
                if await request.is_disconnected():  # Проверяем, разорвано ли соединение
                    break
                yield chunk
    except asyncio.CancelledError:
        pass
    except Exception as e:
        pass


@router.get("/video-stream/{name}")
async def video_stream(name: str, request: Request):
    return StreamingResponse(video_streamer(name, request), media_type="video/mp4")


# @router.get("/url/{name}")
# async def url(name: str):
#     return {
#         "url": f"{settings.API_DOMAIN}/notauth/video-stream/{name}"
#     }