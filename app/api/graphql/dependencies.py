from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.postgresql.database import get_db

db = Annotated[AsyncSession, Depends(get_db)]
