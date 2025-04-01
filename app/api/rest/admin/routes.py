from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from app.api.rest.dependencies import db, user_id
from sqlalchemy import select, delete
from app.postgresql.models import PinsOrm, UsersOrm


router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/{pin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    if user.username != 'danya':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HTTP_403_FORBIDDEN")

    await db.execute(delete(PinsOrm).where(PinsOrm.id == pin_id))
    await db.commit()
    return {"status", "ok"}