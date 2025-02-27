from unittest import mock

import pytest


@pytest.fixture(scope="function")
def mock_revoke_token():
    with mock.patch(
        "app.api.rest.users.routes.revoke_token", new_callable=mock.AsyncMock
    ) as mock_func:
        yield mock_func


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("testUsername", "1234", 201),
        ("testUsername", "1234", 409),
        ("random1", "1235", 201),
        ("random12", "1235", 201),
        ("@random133", "1235", 201),
    ],
)
async def test_auth_flow_users(
    username: str, password: str, status_code: int, ac, mock_revoke_token, mock_is_token_revoked
):
    # /register
    resp_register = await ac.post(
        "/users/register",
        json={
            "username": username,
            "password": password,
        },
    )
    assert resp_register.status_code == status_code
    if status_code != 201:
        return

    # /login
    resp_login = await ac.post(
        "/users/login",
        json={
            "username": username,
            "password": password,
        },
    )
    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    assert ac.cookies["refresh_token"]
    assert "access_token" in resp_login.json()
    assert "refresh_token" in resp_login.json()

    # /me
    resp_me = await ac.get("/users/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user["username"] == username
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    resp_logout = await ac.post("/users/logout")
    assert resp_logout.status_code == 200
    assert "access_token" not in ac.cookies
    assert "refresh_token" not in ac.cookies
