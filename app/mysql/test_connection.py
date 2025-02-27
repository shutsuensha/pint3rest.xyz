from sqlalchemy import text

from app.logger import logger

from .database import get_db


async def connect():
    try:
        async for db in get_db():
            await db.execute(text("SELECT VERSION();"))
            logger.info("✅ Успешное подключение к MySQL")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к MySQL: {e}")
        raise e
