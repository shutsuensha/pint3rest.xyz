## TODO
- refactor routes, imports, add service layer, service layer - work with sqlalchemy, hadle server errors, routes layers - handle fastapi error, documentation for routes
- custom error, middleward - loguru
- fastapi cache
- celery, redis - schedule send email reklama + schedule on db send updated
- user updates - api
- user to user relation
- test
- api documentation
- full rest api for every route
- dockerfile backend, dockerfile frontend, docker-compose
- deploy, nginx, ci/cd
- describe full api in readme do table
- describe repo
- celery results
- rabbitmq
- mongodb
- google one tap, python socialу
- models relations, sqlalchemy work with session example, models on_delete;
- user delete created pins;
- oauth2/jwt secure
- access_token/refresh_token, отзыв токенов
- admin role/api



### Web server
uvicorn app.main:app --reload

### Postgres
psql -U evalshine -d pinterest

### Migrations
alembic revision --autogenerate -m "init"
alembic upgrade head

### Redis
sudo systemctl start redis-server
redis-cli -h localhost -p 6379

### Celery
celery -A app.celery.celery_app.celery_instance worker --loglevel=info
