from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        result = await self.session.exec(statement=statement)
        return result.one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement=statement)
        return result.one_or_none()
