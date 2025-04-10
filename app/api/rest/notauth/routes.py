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