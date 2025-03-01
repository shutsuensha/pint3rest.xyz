FROM python:3.10

# Устанавливаем необходимые системные пакеты
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /pinterest

# Копируем только requirements.txt, чтобы кэшировать зависимости
COPY ./requirements.txt /pinterest/requirements.txt

# Устанавливаем зависимости, если requirements.txt изменился
RUN pip install --no-cache-dir -r /pinterest/requirements.txt

# Копируем остальные файлы
COPY . /pinterest

# Делаем скрипт исполняемым
RUN chmod +x /pinterest/wait-for-db.sh

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN echo "🔥🔥🔥 BUILD СТАДИЯ 🔥🔥🔥"

CMD ["/pinterest/wait-for-db.sh"]
