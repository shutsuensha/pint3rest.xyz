from app.api.rest.dependencies import db
from app.repositories import user_repo

from .exceptions import UserNotFoundError


async def get_user_by_id(db: db, user_id: int):
    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    return user
