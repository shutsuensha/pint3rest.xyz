import pytest
from unittest import mock
from app.api.rest.utils import create_access_token, create_refresh_token, verify_password, hash_password, encode_token, create_url_safe_token, decode_url_safe_token
from fastapi import HTTPException
from itsdangerous import SignatureExpired, BadSignature


@pytest.fixture(scope="function")
def mock_serializer():
    with mock.patch("app.api.rest.utils.serializer") as mock_serializer:
        yield mock_serializer

def test_create_url_safe_token(mock_serializer):
    data = {"user_id": 123}

    mock_serializer.dumps.return_value = "token_string"
    
    result = create_url_safe_token(data)
    
    assert result == "token_string"
    mock_serializer.dumps.assert_called_once_with(data)

def test_decode_url_safe_token_success(mock_serializer):
    token = "token_string"
    expected_data = {"user_id": 123}
    
    mock_serializer.loads.return_value = expected_data
    
    result = decode_url_safe_token(token)
    
    assert result == expected_data
    mock_serializer.loads.assert_called_once_with(token, max_age=3600)

def test_decode_url_safe_token_expired(mock_serializer):
    token = "expired_token"
    
    mock_serializer.loads.side_effect = SignatureExpired("Token has expired")
    
    with pytest.raises(HTTPException) as exc_info:
        decode_url_safe_token(token)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Token has expired"

def test_decode_url_safe_token_invalid(mock_serializer):
    token = "invalid_token"
    
    # Мокаем исключение BadSignature
    mock_serializer.loads.side_effect = BadSignature("Invalid token")
    
    with pytest.raises(HTTPException) as exc_info:
        decode_url_safe_token(token)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid token"
