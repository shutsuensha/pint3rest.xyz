from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException, Query
from app.postgresql.database import get_db
from .utils import encode_token
from app.api.rest.pins.schemas import FilterParams, FilterWithValue
from app.redis.redis_revoke_tokens import is_token_revoked


async def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


async def get_current_user_id(token: Annotated[str, Depends(get_token)]):
    if await is_token_revoked(token):
        raise HTTPException(status_code=401, detail="Token is revoked")
    data = encode_token(token)
    return data["user_id"]


db = Annotated[AsyncSession, Depends(get_db)]
user_id = Annotated[int, Depends(get_current_user_id)]
filter = Annotated[FilterParams, Query()]
filter_with_value = Annotated[FilterWithValue, Query()]