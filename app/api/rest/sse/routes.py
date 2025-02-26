from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import aiofiles
import asyncio
from app.config import settings
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/sse", tags=["sse"])


templates = Jinja2Templates(directory="app/templates")


async def video_streamer():
    async with aiofiles.open(settings.PATH_VIDEO_STREAM, mode="rb") as video:
        while chunk := await video.read(1024 * 1024):  # Читаем чанками по 1MB
            yield chunk  


@router.get("/video-stream")
async def video_stream():
    return StreamingResponse(video_streamer(), media_type="video/mp4")


@router.get("/", response_class=HTMLResponse)
async def ss_template(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="sse.html"
    )