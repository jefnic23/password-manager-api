from typing import Annotated, AsyncGenerator

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings, get_settings
from src.models.refresh_token import RefreshToken  # noqa: F401
from src.models.service import Service  # noqa: F401
from src.models.user import User  # noqa: F401


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class Database:
    def __init__(self, settings: Settings):
        self.engine: AsyncEngine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            future=True,
        )
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )


async def get_database(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Database:
    return Database(settings=settings)


async def get_async_session(
    database: Annotated[Database, Depends(get_database)],
) -> AsyncGenerator[AsyncSession, any]:
    async with database.async_session() as async_session:
        yield async_session


ASYNC_SESSION_DEPENDENCY = Annotated[AsyncSession, Depends(get_async_session)]
