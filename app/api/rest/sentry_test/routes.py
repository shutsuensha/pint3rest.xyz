from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.rest.dependencies import db, user_id
from app.postgresql.models import SearchOrm

router = APIRouter(prefix="/sentry-test", tags=["sentry-test"])


@router.get("/sentry-debug")
async def trigger_zero_division():
    """Искусственная ошибка деления на ноль"""
    division_by_zero = 1 / 0
    return {"result": division_by_zero}


@router.get("/sentry-http-exception")
async def trigger_http_exception():
    """Искусственное возбуждение HTTPException"""
    raise HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        detail="I'm a teapot - тестовая ошибка HTTPException",
    )


@router.get("/sentry-index-error")
async def trigger_index_error():
    """Искусственная ошибка выхода за границы списка"""
    data = [1, 2, 3]
    return {"result": data[5]}  # IndexError


@router.get("/sentry-key-error")
async def trigger_key_error():
    """Искусственная ошибка отсутствующего ключа в словаре"""
    data = {"a": 1, "b": 2}
    return {"result": data["c"]}  # KeyError


@router.get("/sentry-custom-error")
async def trigger_custom_exception():
    """Искусственная пользовательская ошибка"""
    class CustomError(Exception):
        pass

    raise CustomError("Это пользовательская ошибка для теста Sentry")