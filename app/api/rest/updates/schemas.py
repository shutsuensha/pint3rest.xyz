from pydantic import BaseModel
from datetime import datetime

class UpdateResponse(BaseModel):
    id: int
    content: str | None = None
    created_at: datetime
    is_read: bool