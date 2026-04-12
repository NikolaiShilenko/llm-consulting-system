from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase
from app.core.security import decode_token
from app.core.exceptions import InvalidTokenError, TokenExpiredError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    if not token:
        raise InvalidTokenError()

    payload = decode_token(token)
    user_id = int(payload.get("sub"))

    # проверка exp
    exp = payload.get("exp")
    if exp:
        import time
        if exp < int(time.time()):
            raise TokenExpiredError()

    return user_id
