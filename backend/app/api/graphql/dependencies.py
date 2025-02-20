from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.base import get_db


db = Annotated[AsyncSession, Depends(get_db)]