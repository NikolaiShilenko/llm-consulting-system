import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.exceptions import InvalidTokenError


def test_hash_password():
    password = "123456"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_password_correct():
    password = "123456"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    password = "123456"
    wrong_password = "wrong"
    hashed = hash_password(password)
    assert verify_password(wrong_password, hashed) is False


def test_create_access_token():
    token = create_access_token(user_id=1, role="user")
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token_valid():
    token = create_access_token(user_id=1, role="user")
    payload = decode_token(token)
    assert payload["sub"] == "1"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_token_invalid():
    with pytest.raises(InvalidTokenError):
        decode_token("invalid.token.here")
