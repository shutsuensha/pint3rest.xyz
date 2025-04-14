from fastapi import APIRouter, HTTPException, status
from sqlalchemy import insert, select

from app.api.rest.dependencies import db, filter, user_id
from app.postgresql.models import PinsOrm, TagsOrm, pins_tags

from fastapi.responses import FileResponse

from app.api.rest.pins.schemas import PinOut

from .schemas import TagOut, TagsIn


import mimetypes

mimetypes.add_type('image/webp', '.webp')

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tags_on_pin(db: db, user_id: user_id, tags_model: TagsIn):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == tags_model.pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    for tag_name in tags_model.tags:
        tag = await db.scalar(select(TagsOrm).where(TagsOrm.name == tag_name))
        if not tag:
            new_tag = await db.scalar(insert(TagsOrm).values(name=tag_name).returning(TagsOrm))
            await db.execute(insert(pins_tags).values(pin_id=pin.id, tag_id=new_tag.id))
            await db.commit()
        else:
            await db.execute(insert(pins_tags).values(pin_id=pin.id, tag_id=tag.id))
            await db.commit()


@router.get("/", response_model=list[TagOut])
async def get_all_tags(db: db, user_id: user_id):
    tags = await db.scalars(select(TagsOrm))
    return tags


from sqlalchemy import desc

@router.get("/tags-with-first-pin", response_model=list[dict])
async def get_tags_with_first_pin(user_id: user_id, db: db):
    result = []

    # Получаем самый последний пин по id (desc)
    last_pin_stmt = select(PinsOrm).order_by(desc(PinsOrm.id)).limit(1)
    last_pin_result = await db.execute(last_pin_stmt)
    last_pin = last_pin_result.scalar_one_or_none()

    # Добавляем "Everything" первым
    result.append({
        "id": 0,
        "name": "Everything",
        "pinId": last_pin.id if last_pin else None
    })

    # Основные теги
    tags_stmt = select(TagsOrm)
    tags_result = await db.execute(tags_stmt)
    tags = tags_result.scalars().all()

    for tag in tags:
        stmt = (
            select(PinsOrm)
            .join(pins_tags, PinsOrm.id == pins_tags.c.pin_id)
            .where(pins_tags.c.tag_id == tag.id)
            .limit(1)
        )
        pin_result = await db.execute(stmt)
        pin = pin_result.scalar_one_or_none()

        if pin:
            result.append({
                "id": tag.id,
                "name": tag.name,
                "pinId": pin.id
            })

    return result



@router.get("/tags-with-first-pin/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    
    # Определяем MIME тип
    mime_type, _ = mimetypes.guess_type(pin.image)

    # Если MIME тип не определен — задаем вручную
    if mime_type is None:
        if pin.image.endswith('.webp'):
            mime_type = 'image/webp'
        elif pin.image.endswith('.mp4'):
            mime_type = 'video/mp4'
        elif pin.image.endswith('.webm'):
            mime_type = 'video/webm'
        else:
            mime_type = 'application/octet-stream'


    if mime_type in ('video/mp4', 'video/webm'):
        return FileResponse(pin.videoPreview)

    return FileResponse(pin.image, media_type=mime_type)






@router.get("/search/tags-with-first-pin", response_model=list[dict])
async def get_tags_with_first_pin(user_id: user_id, db: db):
    result = []

    # Основные теги, но ограничиваем только первыми 8
    tags_stmt = select(TagsOrm).limit(8)
    tags_result = await db.execute(tags_stmt)
    tags = tags_result.scalars().all()

    for tag in tags:
        stmt = (
            select(PinsOrm)
            .join(pins_tags, PinsOrm.id == pins_tags.c.pin_id)
            .where(pins_tags.c.tag_id == tag.id)
            .limit(1)
        )
        pin_result = await db.execute(stmt)
        pin = pin_result.scalar_one_or_none()

        if pin:
            result.append({
                "id": tag.id,
                "name": tag.name,
                "pinId": pin.id
            })

    return result


@router.get("/{pin_id}")
async def get_related_pins(db: db, user_id: user_id, pin_id: int, filter: filter):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    result = await db.execute(select(pins_tags).where(pins_tags.c.pin_id == pin_id))
    rows = result.all()

    pins = {}

    for row in rows:
        tag_id = row[1]

        new_result = await db.execute(select(pins_tags).where(pins_tags.c.tag_id == tag_id))
        new_rows = new_result.all()

        for new_row in new_rows:
            pin_id = new_row[0]
            pin_db = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
            if pin_db.id not in pins and pin.id != pin_db.id:
                pins[pin_db.id] = pin_db

    return [pin for pin in pins.values()][filter.offset : filter.offset + filter.limit]


@router.get("/pin/tags/{pin_id}", response_model=list[TagOut])
async def get_tags_on_pin(db: db, user_id: user_id, pin_id: int):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    result = await db.execute(select(pins_tags).where(pins_tags.c.pin_id == pin_id))
    rows = result.all()

    tags = []

    for row in rows:
        tag_id = row[1]
        tag = await db.scalar(select(TagsOrm).where(TagsOrm.id == tag_id))
        tags.append(tag)
    return tags
