#!/bin/sh

if [ -f /pinterest/.env ]; then
    export $(grep -v '^#' /pinterest/.env | xargs)
fi

echo "⌛ Ожидание готовности PostgreSQL..."
until pg_isready -h "$POSTGRES_DB_HOST" -p 5432 -U "$POSTGRES_DB_USER" -d "$POSTGRES_DB_NAME"; do
  sleep 2
done
echo "✅ PostgreSQL готов!"

# Применение миграций и запуск сервера
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Если используете прокси-сервер, такой как Nginx или Traefik, добавьте --proxy-headers