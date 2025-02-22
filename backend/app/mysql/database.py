from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings


async_engine = create_async_engine(settings.MYSQL_URL_ASYNC)


async_session = async_sessionmaker(
    async_engine, expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session
