from celery import Celery

celery_instance = Celery(
    "tasks",
    include=["app.celery.tasks"],  # Где искать задачи
)

# Загружаем настройки из файла
celery_instance.config_from_object("app.celery.celeryconfig")