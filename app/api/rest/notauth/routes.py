from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter(prefix="/notauth", tags=["notauth"])


@router.get('/images/{id}')
async def get_image(id: int):
    if id <= 10:
        path = f'{settings.MEDIA_PATH}notauth/{id}.jpg'
    else:
        path = f'{settings.MEDIA_PATH}notauth/{id}.gif'
    return FileResponse(path)