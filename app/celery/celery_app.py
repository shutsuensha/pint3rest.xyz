from datetime import timedelta

from celery import Celery

celery_instance = Celery(
    "tasks",
    include=["app.celery.tasks"], 
)

celery_instance.config_from_object("app.celery.celeryconfig")

celery_instance.conf.beat_schedule = {
    "run-every-10-seconds": {
        "task": "app.celery.tasks.send_email_adds",
        # "schedule": crontab(hour=10, minute=0, day_of_week="sunday")
        "schedule": timedelta(seconds=10)
    },
}