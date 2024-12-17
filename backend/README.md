## Next
- auth with email - redis, celery
- API: users, pins, tags, comments, likes, boards
- writes frontend for API
- refactor routes, imports, add service layer, service layer - work with sqlalchemy, hadle server errors, routes layers - handle fastapi error, documentation for routes
- custom error, middleward - loguru
- fastapi catch
- celery, redis
- test
- dockerfile backend, dockerfile frontend, docker-compose
- deploy, nginx, ci/cd
- describe repo

### Web server
uvicorn app.main:app --reload

### Postgres
psql -U evalshine -d pinterest

### Migrations
alembic revision --autogenerate -m "init"
alembic upgrade head