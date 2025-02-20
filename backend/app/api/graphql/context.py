from .dependencies import db


async def get_context(db: db):
    return {"db": db}