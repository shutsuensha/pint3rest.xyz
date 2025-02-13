from celery import Celery

from app.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL_CELERY,
    include=[
        "app.celery.tasks",
    ],
)