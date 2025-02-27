from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import json
from typing import AsyncGenerator

import pytest
from app.api.rest.users.schemas import UserOut
from app.config import settings
from app.main import app
from app.postgresql.database import get_db
from app.postgresql.models import Base, PinsOrm, UsersOrm
from pydantic import ValidationError
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from httpx import ASGITransport, AsyncClient

engine_null_pool = create_async_engine(settings.TEST_POSTGRES_URL_ASYNC, poolclass=NullPool)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)


async def get_db_null_pool():
    async with async_session_maker_null_pool() as session:
        yield session


@pytest.fixture(scope="function")
async def db():
    async for db in get_db_null_pool():
        yield db



app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_pins.json", encoding="utf-8") as pins_json:
        mock_data = json.load(pins_json)

    async with async_session_maker_null_pool() as session:
        user = UsersOrm(username="test user", hashed_password="hash")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        for pin_data in mock_data:
            pin = PinsOrm(**pin_data, user_id=user.id)
            session.add(pin)
        await session.commit()

    yield

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def mock_is_token_revoked():
    with mock.patch("app.api.rest.dependencies.is_token_revoked", new_callable=mock.AsyncMock) as mock_func:
        mock_func.return_value = False 
        yield mock_func


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    response = await ac.post("/users/register", json={"username": "random-username", "password": "1234"})
    assert response.status_code == 201 

    response_data = response.json()

    try:
        user = UserOut(**response_data)
    except ValidationError as e:
        pytest.fail(f"Response does not match UserOut schema: {e}")

    assert user.username == "random-username"

    return user



@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac, mock_is_token_revoked):
    response = await ac.post("/users/login", json={"username": "random-username", "password": "1234"})
    assert response.status_code == 200
    assert ac.cookies["access_token"]
    assert ac.cookies["refresh_token"]
    yield ac