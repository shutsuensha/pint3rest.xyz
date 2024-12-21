from fastapi import APIRouter, HTTPException, Response, status, UploadFile
from app.api.dependencies import db, user_id, filter
from .schemas import PinOut, PinIn, FilterParams
from app.database.models import PinsOrm
from sqlalchemy import insert, select, update
from app.api.utils import save_file, get_primary_color, extract_first_frame
import uuid
from fastapi.responses import FileResponse


router = APIRouter(prefix="/pins", tags=["pins"])


@router.get('/', response_model=list[PinOut])
async def get_pins(user_id: user_id, db: db, filter: filter):
    pins = await db.scalars(select(PinsOrm).offset(filter.offset).limit(filter.limit))
    return pins


@router.post('/', response_model=PinOut, status_code=status.HTTP_201_CREATED)
async def create_pin(user_id: user_id, db: db, pin_model: PinIn):
    pin = await db.scalar(
        insert(PinsOrm)
        .values(**pin_model.model_dump(), user_id=user_id)
        .returning(PinsOrm)
    )
    await db.commit()
    return pin


@router.post("/upload/{id}", response_model=PinOut)
async def upload_image(user_id: user_id, id: int, db: db, file: UploadFile):

    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"app/media/pins/{unique_filename}"
    save_file(file.file, image_path)

    if file.content_type in ["image/jpeg", "image/png", "image/gif"]:
        rgb = get_primary_color(image_path)
    
    if file.content_type in ["video/mp4", "video/webm", "video/avi"]:
        new_unique_filename = f"{uuid.uuid4()}.jpg"
        new_image_path = f"app/media/pins/{new_unique_filename}"

        extract_first_frame(image_path, new_image_path)
        rgb = get_primary_color(new_image_path)

    pin = await db.scalar(
        update(PinsOrm)
        .where(PinsOrm.id == id)
        .values(image=image_path, rgb=f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
        .returning(PinsOrm)
    )
    await db.commit()

    return pin


@router.get("/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    
    return FileResponse(pin.image)


@router.get("/{id}", response_model=PinOut)
async def get_pin_by_id(user_id: user_id, id: int, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    return pin