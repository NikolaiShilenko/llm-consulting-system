import pytest
from app.core.jwt import decode_and_validate


def test_decode_valid_token(valid_jwt):
    payload = decode_and_validate(valid_jwt)
    assert payload["sub"] == "1"
    assert payload["role"] == "user"


def test_decode_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        decode_and_validate("invalid.token.here")


def test_decode_expired_token(expired_jwt):
    with pytest.raises(ValueError, match="Token expired"):
        decode_and_validate(expired_jwt)
