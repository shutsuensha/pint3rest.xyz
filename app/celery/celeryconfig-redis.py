from app.config import settings  # Загружаем настройки из .env или другого источника

broker_url = settings.REDIS_URL_CELERY_BROKER
result_backend = settings.REDIS_URL_CELERY_RESULT
redbeat_redis_url = settings.REDIS_URL_CELERY_REDBEAT

beat_scheduler = "redbeat.RedBeatScheduler"

task_serializer = "json"
accept_content = ["json"]
result_expires = 3600  # Срок хранения результатов (1 час)
timezone = "UTC"
enable_utc = True
broker_connection_retry_on_startup = True
