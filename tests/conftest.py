import pytest_asyncio
from cryptography.fernet import Fernet
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_async_session
from src.dependencies import get_current_user, get_services_service
from src.main import app
from src.models.user import User
from src.services.services_service import ServicesService

TEST_FERNET_KEY = Fernet.generate_key().decode()
TEST_DATABASE_URL = "sqlite+aiosqlite:///file:testdb?mode=memory&cache=shared&uri=true"

_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
_session_factory = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

USER_ONE = User(id=1, email="user1@test.com", password="hashed")
USER_TWO = User(id=2, email="user2@test.com", password="hashed")


class _TestSettings:
    SECRET_KEY = TEST_FERNET_KEY


@pytest_asyncio.fixture(autouse=True)
async def reset_db():
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def session():
    async with _session_factory() as s:
        yield s


@pytest_asyncio.fixture
async def services_svc(session):
    return ServicesService(session=session, settings=_TestSettings())


def _make_overrides(session: AsyncSession, current_user: User):
    async def _override_session():
        yield session

    def _override_svc():
        return ServicesService(session=session, settings=_TestSettings())

    def _override_user():
        return current_user

    app.dependency_overrides[get_async_session] = _override_session
    app.dependency_overrides[get_services_service] = _override_svc
    app.dependency_overrides[get_current_user] = _override_user


@pytest_asyncio.fixture
async def client(session):
    _make_overrides(session, USER_ONE)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

