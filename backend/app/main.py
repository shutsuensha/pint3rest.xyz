from fastapi import FastAPI
from app.api.users.routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)