## Next
- API: users, pins, tags, comments, likes, boards
- writes frontend for API
- refactor routes, imports, add service layer, service layer - work with sqlalchemy, hadle server errors, routes layers - handle fastapi error, documentation for routes
- custom error, middleward - loguru
- fastapi catch
- celery, redis - schedule send email reklama
- add templates for email
- test
- api documentation
- full rest api for every route
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

### Redis
redis-cli -h localhost -p 6379

### Celery
celery -A app.celery.celery_app.celery_instance worker --loglevel=info