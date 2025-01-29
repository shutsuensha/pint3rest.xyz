from fastapi import APIRouter, HTTPException, Response, status, UploadFile, status
from app.api.dependencies import db, user_id, filter
from .schemas import MessageIn, MessageOut, ChatOut
from app.database.models import ChatOrm, MessageOrm
from sqlalchemy import select, insert, update, func, or_

router = APIRouter(prefix="/messages", tags=["mssagees"])


@router.post('/', status_code=status.HTTP_201_CREATED)
async def user_send_message_in_chat(db: db, user_id: user_id, message: MessageIn):
    if message.chat_id is None:
        chat = await db.scalar(
            insert(ChatOrm)
            .values(user_1_id=user_id, user_2_id=message.to_user_id)
            .returning(ChatOrm)
        )

        message_orm = await db.scalar(
            insert(MessageOrm)
            .values(chat_id=chat.id, user_id_=user_id, content=message.content)
            .returning(MessageOrm)
        )

        await db.commit()
    else:
        chat = await db.scalar(select(ChatOrm).where(ChatOrm.id == message.chat_id))
        if chat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat not found")
        
        message_orm = await db.scalar(
            insert(MessageOrm)
            .values(chat_id=chat.id, user_id_=user_id, content=message.content)
            .returning(MessageOrm)
        )

        await db.commit()


@router.get('/history/{chat_id}', response_model=list[MessageOut])
async def get_chat_history(db: db, user_id: user_id, chat_id: int):
    chat = await db.scalar(select(ChatOrm).where(ChatOrm.id == chat_id))
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat not found")
    messages = await db.scalars(select(MessageOrm).where(MessageOrm.chat_id == chat_id))
    return messages
    
        

@router.get('/check_chat/{user_to_chat}')
async def check_user_get_chat(user_to_chat: int, user_id: user_id, db: db):
    chat = await db.scalar(select(ChatOrm).where(or_(
        (ChatOrm.user_1_id == user_id) & (ChatOrm.user_2_id == user_to_chat),
        (ChatOrm.user_2_id == user_id) & (ChatOrm.user_1_id == user_to_chat)
    )))
    if chat:
        return True
    else:
        return False
    

@router.get('/user_chats', response_model=list[ChatOut])
async def get_users_chat(user_id: user_id, db: db):
    chats = await db.scalars(select(ChatOrm).where(or_(
        ChatOrm.user_1_id == user_id,
        ChatOrm.user_2_id == user_id
    )))
    return chats