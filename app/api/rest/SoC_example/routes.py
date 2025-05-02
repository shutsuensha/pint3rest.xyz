from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.rest.dependencies import db, user_id
from app.postgresql.models import SearchOrm

from app.services import user_service
from app.services.exceptions import UserNotFoundError

router = APIRouter(prefix="/SoC", tags=["SoC"])


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: db):
    try:
        return await user_service.get_user_by_id(db, user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
