import aio_pika
from app.config import settings
from app.logger import logger

rabbitmq_connection = None
rabbitmq_channel = None

async def init_rabbitmq():
    """Инициализация подключения к RabbitMQ."""
    global rabbitmq_connection, rabbitmq_channel
    try:
        rabbitmq_connection = await aio_pika.connect_robust(settings.RABBITMQ_URL_BROKER)
        rabbitmq_channel = await rabbitmq_connection.channel()  # Создаем канал
        logger.info("✅ Успешное подключение к RabbitMQ")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к RabbitMQ: {e}")
        rabbitmq_connection = None
        rabbitmq_channel = None
        raise e
    return rabbitmq_connection, rabbitmq_channel


async def close_rabbitmq():
    """Закрытие подключения к RabbitMQ."""
    global rabbitmq_connection, rabbitmq_channel
    if rabbitmq_channel:
        try:
            await rabbitmq_channel.close()
            logger.info("🔴 Канал RabbitMQ закрыт")
        except Exception as e:
            logger.error(f"Ошибка при закрытии канала RabbitMQ: {e}")

    if rabbitmq_connection:
        try:
            await rabbitmq_connection.close()
            logger.info("🔴 Соединение с RabbitMQ закрыто")
        except Exception as e:
            logger.error(f"Ошибка при закрытии соединения с RabbitMQ: {e}")

async def get_rabbitmq_connection_and_channel():
    """Получить текущее соединение и канал RabbitMQ."""
    global rabbitmq_connection, rabbitmq_channel
    if rabbitmq_connection is None or rabbitmq_channel is None:
        raise Exception("RabbitMQ не подключен. Пожалуйста, инициализируйте соединение.")
    return rabbitmq_connection, rabbitmq_channel