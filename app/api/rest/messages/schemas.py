from datetime import datetime

from pydantic import BaseModel


class MessageIn(BaseModel):
    content: str | None = None
    to_user_id: int | None = None
    chat_id: int | None = None


class MessageOut(BaseModel):
    id: int
    chat_id: int
    user_id_: int
    content: str | None = None
    created_at: datetime
    image: str | None = None
    is_read: bool | None = None


class ChatOut(BaseModel):
    id: int
    user_1_id: int
    user_2_id: int
