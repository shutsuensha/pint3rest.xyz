from unittest import mock

import jwt
import pytest
from app.api.rest.utils import create_access_token, create_refresh_token, encode_token
from app.config import settings
from fastapi import HTTPException


@pytest.fixture(scope="function")
def mock_jwt_encode():
    with mock.patch("app.api.rest.utils.jwt.encode") as mock_encode:
        yield mock_encode


def test_create_access_token(mock_jwt_encode):
    mock_jwt_encode.return_value = "access_token"

    data = {"user_id": 123}
    result = create_access_token(data)
    assert result == "access_token"

    mock_jwt_encode.assert_called_once_with(
        {**data, "exp": mock.ANY, "sub": "access"},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def test_create_refresh_token(mock_jwt_encode):
    mock_jwt_encode.return_value = "refresh_token"

    data = {"user_id": 123}
    result = create_refresh_token(data)

    assert result == "refresh_token"
    mock_jwt_encode.assert_called_once_with(
        {**data, "exp": mock.ANY, "sub": "refresh"},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


@pytest.fixture
def mock_jwt_decode():
    with mock.patch("app.api.rest.utils.jwt.decode") as mock_decode:
        yield mock_decode


def test_encode_token_success(mock_jwt_decode):
    mock_jwt_decode.return_value = {"sub": "access", "exp": "some_expiration"}

    token = "valid_token"
    result = encode_token(token)

    assert result == {"sub": "access", "exp": "some_expiration"}
    mock_jwt_decode.assert_called_once_with(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )


def test_encode_token_expired(mock_jwt_decode):
    mock_jwt_decode.side_effect = jwt.ExpiredSignatureError

    token = "expired_token"

    with pytest.raises(HTTPException) as exc_info:
        encode_token(token)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Token has expired"


def test_encode_token_invalid(mock_jwt_decode):
    mock_jwt_decode.side_effect = jwt.DecodeError

    token = "invalid_token"

    with pytest.raises(HTTPException) as exc_info:
        encode_token(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
