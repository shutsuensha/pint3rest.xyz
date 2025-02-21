from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from app.logger import logger


engine = create_async_engine(settings.POSTGRES_URL_ASYNC)
sync_engine = create_engine(settings.POSTGRES_URL_SYNC)

SyncSession = sessionmaker(bind=sync_engine, expire_on_commit=False)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_maker() as session:
        yield session


def get_sync_db():
    with SyncSession() as session:
        yield session
