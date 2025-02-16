## Time
0/28 - pinterest + tms[tasks, project]

## To Do
- celery beat[mail, database]
- api documentation
- testing
- linter/formatter
- docker
- docker compose
- vps
- domain
- nginx
- ssl
- gitlab ci/cd
- настройка local/remote development
- hard full test project deployed + fix all bugs
- repo descibe


### Web server
sudo systemctl start redis-server
uvicorn app.main:app --reload
celery -A app.celery.celery_app.celery_instance worker --loglevel=info
celery -A app.celery.celery_app.celery_instance flower


### Postgres
psql -U evalshine -d pinterest


### Migrations
alembic revision --autogenerate -m "init"
alembic upgrade head

### Redis
#### Redis celery backend
redis-cli -h localhost -p 6379 -n 0
#### Redis tokens revoke
redis-cli -h localhost -p 6379 -n 1
#### Redis cache
redis-cli -h localhost -p 6379 -n 2
