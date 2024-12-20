from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException, Query
from app.database.base import get_db
from .utils import encode_token
from app.api.pins.schemas import FilterParams



def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="not auth token")
    return token


def get_current_user_id(token: Annotated[str, Depends(get_token)]):
    data = encode_token(token)
    return data["user_id"]


db = Annotated[AsyncSession, Depends(get_db)]
user_id = Annotated[int, Depends(get_current_user_id)]
filter = Annotated[FilterParams, Query()]