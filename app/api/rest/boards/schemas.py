from datetime import datetime

from pydantic import BaseModel


class BoardCreate(BaseModel):
    title: str


class BoardResponse(BoardCreate):
    id: int
    created_at: datetime
