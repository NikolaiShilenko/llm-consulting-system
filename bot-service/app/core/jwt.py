from jose import jwt, JWTError
from app.core.config import settings
import time


def decode_and_validate(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    except JWTError:
        raise ValueError("Invalid token")

    exp = payload.get("exp")
    if exp and exp < int(time.time()):
        raise ValueError("Token expired")

    return payload
