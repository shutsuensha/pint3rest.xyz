## To Do
- token refresh
- token revoke
- middleware loguru
- redis cache
- celery for verification
- celery beat[mail adds]
- celery flower
- api documentation
- docker
- docker compose
- testing
- linter/formatter
- vps
- domain
- nginx
- ssl
- gitlab ci/cd
- repo descibe


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