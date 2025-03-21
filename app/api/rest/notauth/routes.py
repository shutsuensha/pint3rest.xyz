from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import aiofiles
import os
from app.config import settings

router = APIRouter(prefix="/notauth", tags=["notauth"])


@router.get("/images/{id}")
async def get_image(id: int):
    path = f"{settings.MEDIA_PATH}notauth/{id}.jpg"
    return FileResponse(path)


async def range_video_streamer(file_path: str, start: int, end: int):
    async with aiofiles.open(file_path, mode="rb") as video:
        await video.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            chunk_size = min(1024 * 1024, remaining)
            chunk = await video.read(chunk_size)
            if not chunk:
                break
            yield chunk
            remaining -= len(chunk)


@router.get("/video-stream/{name}")
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
    
    return StreamingResponse(range_video_streamer(file_path, start, end), status_code=206, headers=headers)