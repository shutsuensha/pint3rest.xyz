from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
import aiofiles

from app.config import settings

router = APIRouter(prefix="/notauth", tags=["notauth"])


@router.get("/images/{id}")
async def get_image(id: int):
    path = f"{settings.MEDIA_PATH}notauth/{id}.jpg"
    return FileResponse(path)


async def video_streamer(name: str):
    async with aiofiles.open(f"{settings.MEDIA_PATH}/stream/{name}", mode="rb") as video:
        while chunk := await video.read(1024 * 1024):  # Читаем чанками по 1BM
            yield chunk


@router.get("/video-stream/{name}")
async def video_stream(name: str):
    return StreamingResponse(video_streamer(name), media_type="video/mp4")


# @router.get("/url/{name}")
# async def url(name: str):
#     return {
#         "url": f"{settings.API_DOMAIN}/notauth/video-stream/{name}"
#     }