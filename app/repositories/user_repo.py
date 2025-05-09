from sqlalchemy import select

from app.api.rest.dependencies import db
from app.postgresql.models import UsersOrm


async def get_by_id(db: db, user_id: int) -> UsersOrm | None:
    result = await db.execute(select(UsersOrm).where(UsersOrm.id == user_id))
    return result.scalar_one_or_none()
