from fastapi import APIRouter, status
from sqlalchemy import select, update
from fastapi.responses import JSONResponse

from app.api.rest.dependencies import db, user_id
from app.postgresql.models import UsersOrm
from app.websockets.manager import manager

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/color")
async def get_user_chats_color(db: db, user_id: user_id):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user.chat_color


@router.patch("/color", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_chats_color(db: db, user_id: user_id, color: str):
    user = await db.scalar(
        update(UsersOrm).where(UsersOrm.id == user_id).values(chat_color=color).returning(UsersOrm)
    )
    await db.commit()


@router.get("/size")
async def get_user_chats_size(db: db, user_id: user_id):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user.chat_size


@router.patch("/size", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_chats_size(db: db, user_id: user_id, size: int):
    user = await db.scalar(
        update(UsersOrm).where(UsersOrm.id == user_id).values(chat_size=size).returning(UsersOrm)
    )
    await db.commit()


@router.get("/side")
async def get_user_chats_side(db: db, user_id: user_id):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user.side_open


@router.patch("/side", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_chats_side(db: db, user_id: user_id, side: bool):
    user = await db.scalar(
        update(UsersOrm).where(UsersOrm.id == user_id).values(side_open=side).returning(UsersOrm)
    )
    await db.commit()


@router.get("/check_connection/{chat_id}/{user_id}")
async def check_connection(chat_id: int, user_id: int):
    if chat_id not in manager.chats:
        return JSONResponse(content={"active": False})
    if manager.chats[chat_id]["chat_connections"]["user_1"]["user_id"] == user_id or \
        manager.chats[chat_id]["chat_connections"]["user_2"]["user_id"] == user_id:
            return JSONResponse(content={"active": True})
    return JSONResponse(content={"active": False})