## To Do
- mongodb
- websockets .env url ws/wss
- indent format python (zaebalo)
- amazonm s3
- vs code best extantions + .vscode setup for python development
- pytest + aiohttp
- linter/formatter/static typing
- audio/video streaming
- docker
- docker compose
- vps
- domain
- nginx
- ssl
- gitlab ci/cd
- github ci/cd
- настройка local/remote development
- hard full test project deployed + fix all bugs
- repo descibe
- api documentation
- add boards, updates, websocket sending video/image + frontend
- frontend for new message redirect in real time + new chat message + websockets multiply connectings fix
- push notifications
- google social auth
- admin roles checks for rotues that generate information about database state


### Web server
uvicorn app.main:app --reload
celery -A app.celery.celery_app.celery_instance worker --loglevel=info
celery -A app.celery.celery_app.celery_instance flower
celery -A app.celery.celery_app.celery_instance beat --loglevel=info


### Postgres
psql -U evalshine -d pinterest


### Migrations
alembic revision --autogenerate -m "init"
alembic upgrade head


### Redis
#### Redis tokens revoke
redis-cli -h localhost -p 6379 -n 1
#### Redis cache
redis-cli -h localhost -p 6379 -n 2
#### Redis celery BROKER
redis-cli -h localhost -p 6379 -n 3
#### Redis celery RESULT
redis-cli -h localhost -p 6379 -n 4
#### Redis celery REDBEAT
redis-cli -h localhost -p 6379 -n 5