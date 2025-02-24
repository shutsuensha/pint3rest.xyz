from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.postgresql.database import get_db


db = Annotated[AsyncSession, Depends(get_db)]