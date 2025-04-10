from fastapi import APIRouter, HTTPException, status
from sqlalchemy import insert, select

from app.api.rest.dependencies import db, filter, user_id
from app.postgresql.models import PinsOrm, TagsOrm, pins_tags

from .schemas import TagOut, TagsIn

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
