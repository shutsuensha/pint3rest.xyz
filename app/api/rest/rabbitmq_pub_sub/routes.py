import asyncio

import aio_pika
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter(prefix="/rabbitmq-pub-sub", tags=["rabbitmq-pub-sub"])

# Хранилище для всех сообщений в памяти
subscribers = {}  # {queue_name: asyncio.Queue()}


# Подключение и публикация сообщений
async def publish_message(message: str):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL_BROKER)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("test_exchange", aio_pika.ExchangeType.FANOUT)
        await exchange.publish(aio_pika.Message(body=message.encode()), routing_key="")


@router.post("/publish")
async def publish(text: str):
    try:
        await publish_message(text)
        return {"message": f"Message '{text}' published to RabbitMQ!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish message: {e}")


# Прослушивание сообщений и запись их в очередь для SSE
async def listen_for_messages(queue_name: str):
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL_BROKER)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange("test_exchange", aio_pika.ExchangeType.FANOUT)
            queue = await channel.declare_queue(queue_name, durable=True)
            await queue.bind(exchange)

            # Инициализируем очередь сообщений для этой подписки
            subscribers[queue_name] = asyncio.Queue()

            async for message in queue:
                async with message.process():
                    decoded_message = message.body.decode()
                    print(f"[{queue_name}] Получено сообщение: {decoded_message}")
                    await subscribers[queue_name].put(decoded_message)
    except Exception as e:
        print(f"Ошибка при прослушивании очереди {queue_name}: {e}")


# Эндпоинт для запуска подписчика (в фоне)
@router.post("/subscribe")
async def subscribe(queue: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(listen_for_messages, queue)
    return {"message": f"Подписчик для очереди '{queue}' запущен!"}


# SSE Эндпоинт для получения сообщений в реальном времени
@router.get("/subscribe/stream")
async def message_stream(request: Request, queue: str):
    if queue not in subscribers:
        raise HTTPException(status_code=404, detail="Подписчик на такую очередь не запущен")

    async def event_generator():
        while True:
            if await request.is_disconnected():
                print(f"Клиент отключился от очереди {queue}")
                break

            try:
                message = await subscribers[queue].get()
                yield f"data: {message}\n\n"
            except asyncio.CancelledError:
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def get_sse_client(request: Request):
    return templates.TemplateResponse(
        "sse_rabbitmq_pub_sub.html", {"request": request, "API_DOMAIN": settings.API_DOMAIN}
    )
