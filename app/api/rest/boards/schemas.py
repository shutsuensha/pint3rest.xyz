from pydantic import BaseModel
from datetime import datetime

class BoardCreate(BaseModel):
    title: str

class BoardResponse(BoardCreate):
    id: int
    created_at: datetime


class PinsAddRemove(BaseModel):
    pin_ids: list[int]