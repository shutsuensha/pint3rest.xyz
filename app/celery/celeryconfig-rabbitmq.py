from app.config import settings  # Загружаем настройки из .env или другого источника

# Конфигурация брокера сообщений для RabbitMQ
broker_url = settings.RABBITMQ_URL_BROKER
result_backend = (
    settings.RABBITMQ_URL_RESULT
)  # Можно использовать `rpc://` для получения результатов
redbeat_redis_url = settings.REDIS_URL_CELERY_REDBEAT  # Если хотите использовать RedBeat с Redis

beat_scheduler = (
    "redbeat.RedBeatScheduler"  # Используем RedBeat для планирования задач (если необходимо)
)

task_serializer = "json"  # Формат сериализации задач
accept_content = ["json"]  # Разрешаем только формат JSON
result_expires = 3600  # Срок хранения результатов (1 час)
timezone = "UTC"  # Используем UTC
enable_utc = True  # Включаем поддержку UTC

broker_connection_retry_on_startup = True  # Повторное подключение к брокеру при старте
