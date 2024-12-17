from celery import Celery

from app.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "app.celery.tasks",
    ],
)