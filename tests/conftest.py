import contextlib
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

import config as conf
from config import Settings
from models import Base


@pytest.fixture()
async def test_settings() -> Settings:
	test_env = Path(__file__).parent.parent / ".env.test"
	conf.settings = Settings(_env_file=str(test_env))
	return conf.settings


@pytest_asyncio.fixture()
async def db_session(test_settings: Settings) -> AsyncGenerator[AsyncSession, None]:
	"""Start a test database session."""
	engine = create_async_engine(test_settings.db_url)
	session = async_sessionmaker(engine)()
	# session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)()

	# async with session():
	# 	# Clear all tables before each test
	# 	async with session.begin():
	# 		await session.execute(text("PRAGMA foreign_keys = OFF"))
	# 		for table in reversed(Base.metadata.sorted_tables):
	# 			await session.execute(table.delete())
	# 		await session.execute(text("PRAGMA foreign_keys = ON"))
	# 	yield session
	# 	await session.rollback()
	# 	await session.close()

	# TODO : REALIZE THIS
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

	yield session

	await session.rollback()
	await session.close()

	# async with engine.begin() as conn:
	#     await conn.run_sync(Base.metadata.clear())

	"""Remove any data from database (even data not created by this session)"""
	# with contextlib.closing(engine.connect()) as conn:
	#     transaction = conn.begin()
	#     conn.execute(f'TRUNCATE TABLE {",".join(table.name for table in reversed(
	#         Base.metadata.sorted_tables))} RESTART IDENTITY CASCADE;')
	#     transaction.commit()

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
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# yield loop
# loop.close()


def anyio_backend():
	return "asyncio"


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
	"""Create an http client."""
	transport = ASGITransport(app=test_app)
	async with AsyncClient(transport=transport, base_url="http://test") as client:
		yield client
