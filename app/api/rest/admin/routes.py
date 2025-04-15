from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete, select

from app.api.rest.dependencies import db, user_id
from app.postgresql.models import CommentsOrm, PinsOrm, UsersOrm

router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/pin/{pin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    if user.username != "danya":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HTTP_403_FORBIDDEN")

    await db.execute(delete(PinsOrm).where(PinsOrm.id == pin_id))
    await db.commit()
    return {"status", "ok"}


@router.delete("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_copmment(comment_id: int, user_id: user_id, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    if user.username != "danya":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HTTP_403_FORBIDDEN")

    await db.execute(delete(CommentsOrm).where(CommentsOrm.id == comment_id))
    await db.commit()
    return {"status", "ok"}
