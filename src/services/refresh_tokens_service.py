from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.refresh_token import RefreshToken


class RefreshTokensService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_refresh_token(self, user_id: int) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await self.session.exec(statement=statement)
        return result.one_or_none()
