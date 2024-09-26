from pathlib import Path
from unittest import mock
from collections.abc import AsyncGenerator

from dotenv import load_dotenv

import pytest
import pytest_asyncio

from fastapi import FastAPI

from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# import asyncio

from main import app
from config import settings

# from core.db import Base
from core.db.database import get_async_session



import os

test_env = Path(__file__).parent.parent / ".env.test"
load_dotenv(test_env, override=True)

@pytest.fixture(autouse=True)
def print_loaded_env_vars():
    print(f"Loaded test environment variables from: {test_env}")
    for key, value in os.environ.items():
        if key.startswith("POSTGRES_"):
            print(f"{key} = {value}")

# # Overriding the environment file for tests
# @pytest.fixture(scope='session', autouse=True)
# def load_test_env():
#     if test_env.exists():
#         load_dotenv(test_env, override=True)
#         print(f"Loaded test environment variables from: {test_env}")
#     else:
#         raise FileNotFoundError(f"Test .env file not found at: {test_env}")
#
#
# # Mocking the settings to use the test .env during tests
# @pytest.fixture
# def mock_settings_env(monkeypatch):
#     with mock.patch.object(settings.model_config, 'env_file', new=str(Path(__file__).parent.parent / '.env.test')):
#         yield



def pytest_configure(config):
    # This is run before any imports allowing us to inject
    # dependencies via environment variables into Settings
    # This just affects the variables in this process's environment

    # Find the .env file for the test environment
    test_env = str(settings.base_dir / ".env.test")
    # Load the environment variables and overwrite any existing ones
    load_dotenv(test_env, override=True)




@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    db_url = settings.db_url

    # db_name = settings.db_url.split("/")[-1]
    # print(db_url, db_name, "=" * 10)

    engine = create_async_engine(db_url)

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
    app.dependency_overrides[get_async_session] = lambda: db_session
    return app


# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client
