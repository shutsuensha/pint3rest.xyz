import asyncio

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query

from app.config import settings
from redis import asyncio as aioredis
from redis.exceptions import RedisError

router = APIRouter(prefix="/redis-stream", tags=["redis-stream"])


async def get_redis() -> aioredis.Redis:
    return await aioredis.from_url(settings.REDIS_URL_CELERY_BROKER, decode_responses=True)


@router.post("/group/create", summary="Создать Consumer Group в Redis Stream")
async def create_consumer_group(
    stream_name: str = Query("mystream"),
    group_name: str = Query("mygroup"),
    redis: aioredis.Redis = Depends(get_redis),
):
    try:
        await redis.xgroup_create(stream_name, group_name, id="0", mkstream=True)
        return {"message": f"Группа '{group_name}' успешно создана в потоке '{stream_name}'."}
    except RedisError as e:
        if "BUSYGROUP" in str(e):
            raise HTTPException(status_code=400, detail=f"Группа '{group_name}' уже существует.")
        raise HTTPException(status_code=500, detail="Ошибка при создании группы.")


@router.post("/stream/add-message", summary="Добавить сообщение в Redis Stream")
async def add_message_to_stream(
    message: str, stream_name: str = Query("mystream"), redis: aioredis.Redis = Depends(get_redis)
):
    message_id = await redis.xadd(stream_name, {"text": message})
    return {"message": f"Сообщение '{message}' добавлено в поток '{stream_name}' с ID {message_id}."}


async def stream_worker(stream_name: str, group_name: str, consumer_name: str):
    redis = await get_redis()
    try:
        while True:
            messages = await redis.xreadgroup(
                groupname=group_name,
                consumername=consumer_name,
                streams={stream_name: ">"},
                count=1,
                block=5000,  # ждать 5 секунд
            )
            if messages:
                for stream, entries in messages:
                    for message_id, data in entries:
                        print(f"[{consumer_name}] Получил сообщение: {data} с ID: {message_id}")
                        await redis.xack(stream_name, group_name, message_id)
    except asyncio.CancelledError:
        print(f"[{consumer_name}] Воркер остановлен.")


@router.post("/stream/consume", summary="Запустить воркера через BackgroundTasks")
async def consume_stream(
    background_tasks: BackgroundTasks,
    consumer_name: str = Query("worker-1"),
    stream_name: str = Query("mystream"),
    group_name: str = Query("mygroup"),
):
    background_tasks.add_task(stream_worker, stream_name, group_name, consumer_name)
    return {
        "message": f"Воркер '{consumer_name}' запущен в фоне для потока '{stream_name}' и группы '{group_name}'."
    }


@router.get("/stream/messages", summary="Получить все сообщения из потока")
async def get_stream_messages(
    stream_name: str = Query("mystream"),
    count: int = Query(10, description="Максимальное количество сообщений для получения"),
    redis: aioredis.Redis = Depends(get_redis),
):
    try:
        # Получаем сообщения с самого начала потока
        messages = await redis.xrange(stream_name, count=count)
        formatted_messages = [
            {"id": message_id, "data": data}
            for message_id, data in messages
        ]
        return {"stream": stream_name, "messages": formatted_messages}
    except RedisError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении сообщений: {str(e)}")