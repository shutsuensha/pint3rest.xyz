from celery import Celery
from celery.schedules import crontab
from app.logger import logger
from datetime import timedelta


celery_instance = Celery(
    "tasks",
    include=["app.celery.tasks"], 
)

celery_instance.config_from_object("app.celery.celeryconfig")

celery_instance.conf.beat_schedule = {
    "run-every-10-seconds": {
        "task": "app.celery.tasks.send_email_adds",
        "schedule": crontab(hour=10, minute=0, day_of_week="sunday")
    },
}