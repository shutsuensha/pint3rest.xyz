import strawberry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError

from app.postgresql.models import UsersOrm

from .schemas import User


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, username: str, info: strawberry.Info) -> User:
        db: AsyncSession = info.context["db"]

        existing_user = await db.execute(
            select(UsersOrm).filter(UsersOrm.username == username)
        )
        user = existing_user.scalars().first()

        if user:
            raise GraphQLError(f"User with username '{username}' already exists")

        new_user = UsersOrm(username=username, hashed_password="example password")
        db.add(new_user)
        await db.commit()

        return User(id=new_user.id, username=new_user.username)

    @strawberry.mutation
    async def update_user_username(
        self, user_id: int, new_username: str, info: strawberry.Info
    ) -> User:
        db: AsyncSession = info.context["db"]

        user = await db.get(UsersOrm, user_id)
        if not user:
            raise GraphQLError(f"User with id '{id}' not found")

        user.username = new_username
        await db.commit()
        await db.refresh(user)

        return User(id=user.id, username=user.username)

    @strawberry.mutation
    async def delete_user(self, user_id: int, info: strawberry.Info) -> str:
        db: AsyncSession = info.context["db"]
        user = await db.get(UsersOrm, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            return "deleted: ok"
        raise GraphQLError(f"User with id '{user_id}' not found")
