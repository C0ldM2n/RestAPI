from pathlib import Path
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio

from fastapi import FastAPI

from httpx import AsyncClient, ASGITransport


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import config as conf
from config import Settings


@pytest.fixture()
async def test_settings() -> Settings:
    test_env = Path(__file__).parent.parent / ".env.test"
    conf.settings = Settings(_env_file=str(test_env))
    return conf.settings


@pytest_asyncio.fixture()
async def db_session(test_settings: Settings) -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    db_url = Settings.db_url
    engine = create_async_engine(test_settings.db_url)

    # TODO : REALIZE THIS
    # only for dev
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    from main import app
    from core.db.database import get_async_session
    app.dependency_overrides[get_async_session] = lambda: db_session
    return app


# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
