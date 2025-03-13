import asyncio
import json
import uuid
from typing import Dict

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import ValidationError
from sqlalchemy import desc, func, insert, or_, select, update

from app.api.rest.dependencies import db, filter, user_id
from app.api.rest.utils import save_file
from app.config import settings
from app.postgresql.models import ChatOrm, MessageOrm

from .schemas import ChatOut, MessageIn, MessageOut

router = APIRouter(prefix="/messages", tags=["messages"])

active_connections: Dict[int, asyncio.Queue] = {}


async def event_stream(user_id: int):
    queue = asyncio.Queue()
    active_connections[user_id] = queue

    try:
        while True:
            message = await queue.get()  # Ждем нового сообщения для пользователя
            yield f"data: {json.dumps({'message': message})}\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        del active_connections[user_id]  # Удаляем соединение при закрытии


@router.get("/stream/{user_id}")
async def stream(user_id: int):
    return StreamingResponse(event_stream(user_id), media_type="text/event-stream")


@router.post("/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
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
        if message.to_user_id in active_connections:
            queue = active_connections[message.to_user_id]
            await queue.put({"chat_id": chat.id})

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
    return message_orm


@router.post(
    "/create-message-entity", response_model=MessageOut, status_code=status.HTTP_201_CREATED
)
async def create_message_entity(
    db: db, user_id: user_id, message: str = Form(...), file: UploadFile = File(...)
):
    try:
        message = json.loads(message)
        message = MessageIn(**message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {e.errors()}")

    chat = await db.scalar(select(ChatOrm).where(ChatOrm.id == message.chat_id))
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat not found")

    message_orm = await db.scalar(
        insert(MessageOrm)
        .values(chat_id=chat.id, user_id_=user_id, content=message.content)
        .returning(MessageOrm)
    )

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"{settings.MEDIA_PATH}messages/{unique_filename}"
    await save_file(file.file, image_path)

    message_orm = await db.scalar(
        update(MessageOrm)
        .where(MessageOrm.id == message_orm.id)
        .values(image=image_path)
        .returning(MessageOrm)
    )
    await db.commit()

    return message_orm


@router.get("/history/{chat_id}", response_model=list[MessageOut])
async def get_chat_history(db: db, user_id: user_id, chat_id: int, filter: filter):
    chat = await db.scalar(select(ChatOrm).where(ChatOrm.id == chat_id))
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat not found")
    messages = await db.scalars(
        select(MessageOrm)
        .where(MessageOrm.chat_id == chat_id)
        .order_by(MessageOrm.id.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )
    return messages


@router.get("/last/{chat_id}", response_model=MessageOut)
async def get_last_message_in_chat(db: db, user_id: user_id, chat_id: int):
    chat = await db.scalar(select(ChatOrm).where(ChatOrm.id == chat_id))
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat not found")

    message = await db.scalar(
        select(MessageOrm)
        .where(MessageOrm.chat_id == chat_id)
        .order_by(desc(MessageOrm.id))
        .limit(1)
    )

    return message


@router.get("/check_chat/{user_to_chat}")
async def check_user_get_chat(user_to_chat: int, user_id: user_id, db: db):
    chat = await db.scalar(
        select(ChatOrm).where(
            or_(
                (ChatOrm.user_1_id == user_id) & (ChatOrm.user_2_id == user_to_chat),
                (ChatOrm.user_2_id == user_id) & (ChatOrm.user_1_id == user_to_chat),
            )
        )
    )
    if chat:
        return True
    else:
        return False


@router.get("/get_chat/{user_to_chat}")
async def user_get_chat(user_to_chat: int, user_id: user_id, db: db):
    chat = await db.scalar(
        select(ChatOrm).where(
            or_(
                (ChatOrm.user_1_id == user_id) & (ChatOrm.user_2_id == user_to_chat),
                (ChatOrm.user_2_id == user_id) & (ChatOrm.user_1_id == user_to_chat),
            )
        )
    )
    return chat.id


@router.get("/user_chats", response_model=list[ChatOut])
async def get_users_chat(user_id: user_id, db: db):
    chats = await db.scalars(
        select(ChatOrm).where(or_(ChatOrm.user_1_id == user_id, ChatOrm.user_2_id == user_id))
    )
    return chats


@router.get("/get_chat_by_id/{chat_id}", response_model=ChatOut)
async def get_user_chat_by_id(user_id: user_id, db: db, chat_id: int):
    chat = await db.scalar(select(ChatOrm).where(ChatOrm.id == chat_id))
    return chat


@router.post("/upload/{id}", response_model=MessageOut)
async def upload_image(user_id: user_id, id: int, db: db, file: UploadFile):
    message = await db.scalar(select(MessageOrm).where(MessageOrm.id == id))
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="message not found")

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"{settings.MEDIA_PATH}messages/{unique_filename}"
    await save_file(file.file, image_path)

    message = await db.scalar(
        update(MessageOrm).where(MessageOrm.id == id).values(image=image_path).returning(MessageOrm)
    )
    await db.commit()

    return message


@router.get("/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    message = await db.scalar(select(MessageOrm).where(MessageOrm.id == id))
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="message not found")

    return FileResponse(message.image)


@router.get("/unread/cnt/{chat_id}")
async def get_user_chat_unread_messages(user_id: user_id, db: db, chat_id: int):
    cnt_messages = await db.scalar(
        select(func.count()).where(
            MessageOrm.chat_id == chat_id,
            MessageOrm.is_read == False,
            MessageOrm.user_id_ != user_id,
        )
    )
    return cnt_messages


@router.patch("/read/{message_id}", response_model=MessageOut)
async def user_read_message(user_id: user_id, db: db, message_id: int):
    message = await db.scalar(
        update(MessageOrm)
        .where(MessageOrm.id == message_id)
        .values(is_read=True)
        .returning(MessageOrm)
    )
    await db.commit()
    return message


@router.get("/unread/all_chats/cnt")
async def get_user_all_chats_unread_messages(user_id: user_id, db: db):
    chat_ids_subquery = (
        select(ChatOrm.id)
        .where((ChatOrm.user_1_id == user_id) | (ChatOrm.user_2_id == user_id))
        .subquery()
    )

    cnt_messages = await db.scalar(
        select(func.count(MessageOrm.id)).where(
            MessageOrm.chat_id.in_(select(chat_ids_subquery)),
            MessageOrm.user_id_ != user_id,
            MessageOrm.is_read == False,
        )
    )
    return cnt_messages
