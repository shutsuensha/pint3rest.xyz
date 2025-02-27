import uuid

from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import delete, desc, insert, or_, select, update

from app.api.rest.dependencies import db, filter, filter_with_value, user_id
from app.api.rest.tags.routes import get_all_tags
from app.api.rest.utils import extract_first_frame, get_primary_color, save_file
from app.config import settings
from app.postgresql.models import LikesOrm, PinsOrm, TagsOrm, UsersOrm, pins_tags, users_pins

from .schemas import PinIn, PinOut

router = APIRouter(prefix="/pins", tags=["pins"])


@router.get('/', response_model=list[PinOut])
async def get_pins(user_id: user_id, db: db, filter: filter):

    pins = await db.scalars(
        select(PinsOrm)
        .offset(filter.offset)
        .limit(filter.limit)
        .order_by(desc(PinsOrm.id))
    )

    return pins


@router.get('/tag/{tag_name}', response_model=list[PinOut])
async def get_pins_by_tag(tag_name: str, user_id: user_id, db: db, filter: filter):
    tag = await db.scalar(select(TagsOrm).where(TagsOrm.name == tag_name))
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag not found")

    result = await db.execute(select(pins_tags).where(pins_tags.c.tag_id == tag.id))
    rows = result.all()
    pins = []
    for row in rows:
        pin_id = row[0]
        pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
        pins.append(pin)
    return pins[filter.offset:filter.offset+filter.limit]


@router.get('/search', response_model=list[PinOut])
async def search_pins(filter_with_value: filter_with_value, user_id: user_id, db: db):
    result = {}

    split_and_clean = [part for part in filter_with_value.value.split(' ') if part.strip()]
    tags = await get_all_tags(db, user_id)
    tag_list = tags.all()
    for value in split_and_clean:
        pins = await db.scalars(select(PinsOrm).where(
                or_(
                    PinsOrm.title.ilike(f"%{value}%"),
                    PinsOrm.description.ilike(f"%{value}%")    
                )
            )
        )
        pin_list = pins.all()
        for pin in pin_list:
            if pin.id not in result:
                result[pin.id] = pin

        for tag in tag_list:
            if value in tag.name:
                    tag = await db.scalar(select(TagsOrm).where(TagsOrm.name == tag.name))
                    result_table = await db.execute(select(pins_tags).where(pins_tags.c.tag_id == tag.id))
                    rows = result_table.all()
                    for row in rows:
                        pin_by_tag_id = row[0]
                        if pin_by_tag_id not in result:
                            pin_by_tag = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_by_tag_id))
                            result[pin_by_tag.id] = pin_by_tag


    return [pin for pin in result.values()][filter_with_value.offset:filter_with_value.offset+filter_with_value.limit]



@router.post('/', response_model=PinOut, status_code=status.HTTP_201_CREATED)
async def create_pin(user_id: user_id, db: db, pin_model: PinIn):
    pin = await db.scalar(
        insert(PinsOrm)
        .values(**pin_model.model_dump(), user_id=user_id)
        .returning(PinsOrm)
    )
    await db.commit()
    return pin


@router.delete('/{pin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_created_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    await db.execute(delete(PinsOrm).where(PinsOrm.user_id == user_id, PinsOrm.id == pin_id))
    await db.commit()
    return {'status', 'ok'}


@router.post("/upload/{id}", response_model=PinOut)
async def upload_image(user_id: user_id, id: int, db: db, file: UploadFile):

    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"{settings.MEDIA_PATH}pins/{unique_filename}"
    save_file(file.file, image_path)

    if file.content_type in ["image/jpeg", "image/png", "image/gif"]:
        rgb = get_primary_color(image_path)
    
    if file.content_type in ["video/mp4", "video/webm", "video/avi"]:
        new_unique_filename = f"{uuid.uuid4()}.jpg"
        new_image_path = f"{settings.MEDIA_PATH}pins/{new_unique_filename}"

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


@router.get('/user_created_pins/{id}', response_model=list[PinOut])
async def get_user_created_pins(id: int, user_id: user_id, db: db, filter: filter):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    pins = await db.scalars(select(PinsOrm).where(PinsOrm.user_id == id).offset(filter.offset).limit(filter.limit))
    return pins


@router.post('/user_saved_pins/{pin_id}', status_code=status.HTTP_201_CREATED)
async def user_save_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    
    query = select(users_pins).where(users_pins.c.user_id == user_id, users_pins.c.pin_id == pin_id)
    result = await db.execute(query)
    user_pin = result.fetchone()  # Use `.fetchone()` to get a single result

    if user_pin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already saved this pin")

    await db.execute(insert(users_pins).values(user_id=user_id, pin_id=pin_id))
    await db.commit()
    return {'status', 'ok'}


@router.delete('/user_saved_pins/{pin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_saved_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    await db.execute(delete(users_pins).where(users_pins.c.user_id == user_id, users_pins.c.pin_id == pin_id))
    await db.commit()
    return {'status', 'ok'}


@router.get('/user_saved_pins/{id}', response_model=list[PinOut])
async def get_user_saved_pins(id: int, user_id: user_id, db: db, filter: filter):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    result = await db.execute(select(users_pins).where(users_pins.c.user_id == id).offset(filter.offset).limit(filter.limit))
    rows = result.all()
    pins = []
    for row in rows:
        pin_id = row[1]
        pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
        pins.append(pin)
    return pins


@router.get('/user_liked_pins/{id}', response_model=list[PinOut])
async def get_user_liked_pins(id: int, user_id: user_id, db: db, filter: filter):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    result = await db.execute(
        select(PinsOrm)
        .join(LikesOrm, PinsOrm.id == LikesOrm.pin_id)
        .where(LikesOrm.user_id == id)
        .offset(filter.offset)
        .limit(filter.limit)
    )
    pins = result.scalars().all()

    return pins