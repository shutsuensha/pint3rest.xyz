from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.logger import logger


class MongoDB:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = None
        self.db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client.get_database()
            logger.info("✅ Успешное подключение к MongoDB")
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к MongoDB: {e}")
            raise e

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("🔴 Соединение с MongoDB закрыто")

    def get_collection(self, name: str):
        return self.db[name]


mongo = MongoDB(settings.MONGO_URL)
