from pydantic import BaseModel
from datetime import datetime


class UpdateResponse(BaseModel):
    id: int
    content: str | None = None
    created_at: datetime
    is_read: bool
    update_type: str
    user_id: int | None = None
    pin_id: int | None = None
    comment_id: int | None = None
    reply_id: int | None = None