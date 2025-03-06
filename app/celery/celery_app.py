from datetime import timedelta  # noqa

from celery import Celery
from celery.schedules import crontab

celery_instance = Celery(
    "tasks",
    include=["app.celery.tasks"],
)

celery_instance.config_from_object("app.celery.celeryconfig")

celery_instance.conf.beat_schedule = {
    "mail-adds": {
        "task": "app.celery.tasks.send_email_adds",
        # "schedule": crontab(hour=10, minute=0, day_of_week="sunday"),
        "schedule": timedelta(seconds=10),
    },
}
