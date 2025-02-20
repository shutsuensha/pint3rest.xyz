from fastapi import APIRouter, HTTPException, Response, status, UploadFile
from app.api.rest.dependencies import db, user_id, filter
from sqlalchemy import select, insert, update, func
from app.database.models import UsersOrm


router = APIRouter(prefix="/chats", tags=["chats"])


@router.get('/color')
async def get_user_chats_color(db: db, user_id: user_id):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user.chat_color


@router.patch('/color', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_chats_color(db: db, user_id: user_id, color: str):
    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == user_id)
        .values(chat_color = color)
        .returning(UsersOrm)
    )
    await db.commit()


@router.get('/size')
async def get_user_chats_size(db: db, user_id: user_id):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user.chat_size


@router.patch('/size', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_chats_size(db: db, user_id: user_id, size: int):
    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == user_id)
        .values(chat_size = size)
        .returning(UsersOrm)
    )
    await db.commit()



@router.get('/side')
async def get_user_chats_side(db: db, user_id: user_id):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user.side_open


@router.patch('/side', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_chats_side(db: db, user_id: user_id, side: bool):
    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == user_id)
        .values(side_open = side)
        .returning(UsersOrm)
    )
    await db.commit()