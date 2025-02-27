from unittest import mock

import pytest
from app.api.rest.utils import hash_password, verify_password


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

