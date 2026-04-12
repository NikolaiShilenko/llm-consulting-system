from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError
from app.repositories.users import UserRepository


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str):
        existing = await self._user_repo.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError()

        hashed = hash_password(password)
        user = await self._user_repo.create(email, hashed)
        return user

    async def login(self, email: str, password: str) -> str:
        user = await self._user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return create_access_token(user.id, user.role)

    async def get_profile(self, user_id: int):
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user
