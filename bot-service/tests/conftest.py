import pytest
from unittest.mock import AsyncMock, patch
from app.core.config import settings


@pytest.fixture
def mock_redis():
    with patch("app.infra.redis.get_redis") as mock:
        redis_mock = AsyncMock()
        mock.return_value = redis_mock
        yield redis_mock


@pytest.fixture
def valid_jwt():
    from jose import jwt
    from datetime import datetime, timedelta, timezone

    payload = {
        "sub": "1",
        "role": "user",
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=60)).timestamp())
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


@pytest.fixture
def expired_jwt():
    from jose import jwt
    from datetime import datetime, timedelta, timezone

    payload = {
        "sub": "1",
        "role": "user",
        "iat": int((datetime.now(timezone.utc) - timedelta(hours=2)).timestamp()),
        "exp": int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp())
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
