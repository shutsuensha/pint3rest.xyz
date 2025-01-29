from pydantic import BaseModel
from datetime import datetime


class MessageIn(BaseModel):
    content: str
    to_user_id: int | None = None
    chat_id: int | None = None


class MessageOut(BaseModel):
    id: int
    chat_id: int
    user_id_: int
    content: str
    created_at: datetime


class ChatOut(BaseModel):
    id: int
    user_1_id: int
    user_2_id: int