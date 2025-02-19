from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(prefix="/notauth", tags=["notauth"])


@router.get('/images/{id}')
async def get_image(id: int):
    if id <= 10:
        path = f'app/media/notauth/{id}.jpg'
    else:
        path = f'app/media/notauth/{id}.gif'
    return FileResponse(path)