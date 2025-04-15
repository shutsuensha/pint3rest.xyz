from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.rest.dependencies import db, filter, user_id
from app.postgresql.models import UpdatesOrm

from .schemas import UpdateResponse

router = APIRouter(prefix="/updates", tags=["updates"])


@router.get("/count")
async def get_updates_count(user_id: user_id, db: db):
    result = await db.execute(
        select(UpdatesOrm).where(
            UpdatesOrm.user_update_to_id == user_id, UpdatesOrm.is_read == False
        )
    )
    return len(result.fetchall())


@router.get("/", response_model=list[UpdateResponse])
async def get_updates(user_id: user_id, db: db, filter: filter):
    result = await db.execute(
        select(UpdatesOrm)
        .where(UpdatesOrm.user_update_to_id == user_id)
        .order_by(UpdatesOrm.created_at.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )
    return result.scalars().all()


@router.get("/{update_id}", response_model=UpdateResponse)
async def get_update_by_id(update_id: int, user_id: user_id, db: db):
    stmt = select(UpdatesOrm).filter(UpdatesOrm.id == update_id)
    result = await db.execute(stmt)
    update = result.scalars().first()
    return update


@router.put("/read/{update_id}")
async def mark_update_as_read(update_id: int, db: db):
    result = await db.execute(select(UpdatesOrm).where(UpdatesOrm.id == update_id))
    update = result.scalars().first()

    if not update:
        raise HTTPException(status_code=404, detail="Update not found")

    update.is_read = True
    await db.commit()
