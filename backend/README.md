## To Do
- middleware loguru / logging
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
#### Redis celery backend
redis-cli -h localhost -p 6379 -n 0
#### Redis tokens revoke
redis-cli -h localhost -p 6379 -n 1
#### Redis cache
redis-cli -h localhost -p 6379 -n 2


### Celery
celery -A app.celery.celery_app.celery_instance worker --loglevel=info