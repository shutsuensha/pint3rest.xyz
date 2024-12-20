from fastapi import FastAPI
from app.api.users.routes import router as auth_router
from app.api.pins.routes import router as pin_router

app = FastAPI()

app.include_router(pin_router)
app.include_router(auth_router)