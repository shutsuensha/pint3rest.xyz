import aio_pika
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.rabbitmq.app import get_rabbitmq_connection_and_channel

router = APIRouter(prefix="/rabbitmq-stream", tags=["rabbitmq-stream"])


# Роут для отправки сообщений в очередь RabbitMQ
@router.post("/send")
async def send_message(message: str):
    try:
        # Получаем соединение и канал RabbitMQ
        connection, channel = await get_rabbitmq_connection_and_channel()

        # Отправляем сообщение в очередь
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()), routing_key="messages"
        )

        return {"status": "message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Роут для получения всех сообщений из очереди RabbitMQ
@router.get("/read")
async def read_messages():
    try:
        # Получаем соединение и канал RabbitMQ
        connection, channel = await get_rabbitmq_connection_and_channel()

        # Объявляем очередь и читаем все сообщения
        queue = await channel.declare_queue("messages", durable=True)
        messages = []

        # Лимит на количество сообщений, чтобы избежать бесконечного чтения
        message_limit = 10  # Пример: читаем максимум 10 сообщений
        count = 0

        async for message in queue:
            if count >= message_limit:
                break
            async with message.process():
                messages.append(message.body.decode())
                count += 1

        # Возвращаем все сообщения
        return JSONResponse(content={"messages": messages})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
