
from app.config import settings  # Загружаем настройки из .env или другого источника

broker_url = settings.REDIS_URL_CELERY  # Например, redis://localhost:6379/0
result_backend = settings.REDIS_URL_CELERY

task_serializer = "json"
accept_content = ["json"]
result_expires = 3600  # Срок хранения результатов (1 час)
timezone = "UTC"
enable_utc = True
broker_connection_retry_on_startup = True
