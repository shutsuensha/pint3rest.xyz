from app.api.rest.utils import create_access_token, create_refresh_token, verify_password, hash_password, encode_token, create_url_safe_token, decode_url_safe_token
import pytest
from unittest import mock
from app.config import settings
import jwt
from fastapi import HTTPException
from itsdangerous import SignatureExpired, BadSignature

@pytest.fixture(scope="function")
def mock_pwd_context():
    with mock.patch("app.api.rest.utils.pwd_context") as mock_ctx:
        yield mock_ctx

def test_hash_password(mock_pwd_context):
    mock_pwd_context.hash.return_value = "hashed_password"
    
    result = hash_password("password")
    
    assert result == "hashed_password"
    mock_pwd_context.hash.assert_called_once_with("password")

def test_verify_password(mock_pwd_context):
    mock_pwd_context.verify.return_value = True
    
    result = verify_password("password", "hashed_password")
    
    assert result is True
    mock_pwd_context.verify.assert_called_once_with("password", "hashed_password")

