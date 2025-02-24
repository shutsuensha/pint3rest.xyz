import strawberry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError
from .schemas import User
from app.postgresql.models import UsersOrm


@strawberry.type
class Query:
    @strawberry.field
    async def get_users(self, info: strawberry.Info) -> list[User]:
        db: AsyncSession = info.context["db"]
        users = await db.scalars(select(UsersOrm))
        return [User(id=user.id, username=user.username) for user in users]

    @strawberry.field
    async def get_user_by_id(self, user_id: int, info: strawberry.Info) -> User:
        db: AsyncSession = info.context["db"]
        user = await db.get(UsersOrm, user_id)
        if user:
            return User(id=user.id, username=user.username)
        raise GraphQLError(f"User with id '{user_id}' not found")
