from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.users.routes import router as auth_router
from app.api.pins.routes import router as pin_router
from app.api.tags.routes import router as tag_router
from app.api.comments.routes import router as comment_router
from app.api.likes.routes import router as like_router

app = FastAPI()

app.include_router(pin_router)
app.include_router(tag_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(auth_router)


@app.get('/index/notauth/images/{id}')
async def get_image(id: int):
    if id <= 10:
        return FileResponse(f'app/media/carousel/{id}.jpg')
    else:
        return FileResponse(f'app/media/carousel/{id}.gif')