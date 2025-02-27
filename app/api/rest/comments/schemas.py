from datetime import datetime

from pydantic import BaseModel


class CommentIn(BaseModel):
    content: str | None = None


class CommentOut(BaseModel):
    id: int
    pin_id: int | None = None
    user_id: int
    comment_id: int | None = None
    content: str | None = None
    created_at: datetime
    image: str | None = None
