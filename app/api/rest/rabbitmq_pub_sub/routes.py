import aio_pika
from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.config import settings

router = APIRouter(prefix="/rabbitmq-pub-sub", tags=["rabbitmq-pub-sub"], include_in_schema=False)


# Публикация сообщения в RabbitMQ
async def publish_message(message: str):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL_BROKER)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("test_exchange", aio_pika.ExchangeType.FANOUT)
        # Убедитесь, что routing_key пустой, так как для FANOUT он не требуется
        await exchange.publish(aio_pika.Message(body=message.encode()), routing_key="")


@router.post("/publish")
async def publish(text: str):
    try:
        await publish_message(text)
        return {"message": f"Message '{text}' published to RabbitMQ!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish message: {e}")


# Прослушивание сообщений
async def listen_for_messages(queue_name: str):
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL_BROKER)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange("test_exchange", aio_pika.ExchangeType.FANOUT)
            queue = await channel.declare_queue(
                queue_name, durable=True
            )  # Убедитесь, что очередь durable
            await queue.bind(exchange)

            print("Subscriber started listening to messages...")

            # Обработка сообщений
            async for message in queue:
                async with message.process():
                    print(f"{queue_name} - Received message: {message.body.decode()}")
    except Exception as e:
        print(f"Error listening to messages: {e}")


# Функция для асинхронного запуска подписчика
async def run_subscriber(queue: str):
    await listen_for_messages(queue)


@router.post("/subscribe")
async def subscribe(queue: str, background_tasks: BackgroundTasks):
    # Запускаем подписчика в фоне
    background_tasks.add_task(run_subscriber, queue)
    return {"message": "Subscriber started listening to messages!"}
