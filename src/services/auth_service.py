from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.exceptions import credentials_exception
from src.models.refresh_token import RefreshToken
from src.models.user import User
from src.services.refresh_tokens_service import RefreshTokensService
from src.services.users_service import UsersService


class AuthService:
    PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(
        self,
        session: AsyncSession,
        settings: Settings,
        users_service: UsersService,
        refresh_tokens_service: RefreshTokensService,
    ):
        self.session = session
        self.settings = settings
        self.users_service = users_service
        self.refresh_tokens_service = refresh_tokens_service

    async def authenticate_user(self, email: str, password: str) -> User | bool:
        user = await self.users_service.get_user_by_email(email=email)
        if not user:
            return False
        if not AuthService.verify_password(secret=password, hash=user.password):
            return False
        return user

    def generate_access_token(self, sub: int, expiry_minutes: int = 5) -> str:
        exp = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
        claims = {
            "exp": exp,
            "sub": str(sub),
        }
        return jwt.encode(
            claims=claims,
            key=self.settings.SECRET_KEY,
            algorithm="HS256",
        )

    async def generate_refresh_token(
        self, sub: int, expiry_minutes: int = 43200
    ) -> str:
        exp = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
        claims = {
            "exp": exp,
            "sub": str(sub),
        }
        token = jwt.encode(
            claims=claims,
            key=self.settings.SECRET_KEY,
            algorithm="HS256",
        )
        refresh_token = await self.refresh_tokens_service.get_refresh_token(user_id=sub)
        if not refresh_token:
            refresh_token = RefreshToken(token=token, expiry_time=exp, user_id=sub)
            self.session.add(refresh_token)
        else:
            refresh_token.token = token
            refresh_token.expiry_time = exp
        await self.session.commit()
        return token

    def verify_token(
        self, token: str, exception: HTTPException = credentials_exception
    ) -> dict[str, any]:
        try:
            payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=["HS256"])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise exception
        except JWTError:
            raise exception
        return payload

    @staticmethod
    def verify_password(
        secret: str, hash: str, password_context: CryptContext = PASSWORD_CONTEXT
    ) -> bool:
        return password_context.verify(secret=secret, hash=hash)

    @staticmethod
    def hash_password(
        secret: str, password_context: CryptContext = PASSWORD_CONTEXT
    ) -> str:
        return password_context.hash(secret=secret)
