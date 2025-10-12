from pathlib import Path
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import settings


class Database:
    """Class for actions related to connecting to database"""

    def __init__(self, db_url: str, debug: bool):
        alembic_ini_path = (
            Path(__file__).resolve().parent.parent.parent.parent / "alembic.ini"
        )

        self._engine: AsyncEngine = create_async_engine(
            db_url,
            echo="debug" if debug else False,
            # max_overflow=10
        )
        self._SessionMaker = async_sessionmaker(self._engine, expire_on_commit=False)

        self._alembic_cfg = Config(str(alembic_ini_path))

    @property
    def engine(self) -> AsyncEngine:
        """Expose the underlying engine for operations that need direct access."""
        return self._engine

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Method for obtaining a session"""

        async with self._SessionMaker() as session:
            try:
                yield session
            finally:
                await session.close()

    async def connect(self) -> None:
        """Method for opening a connection to database."""

        # First verification request to database
        async with self._engine.begin() as conn:
            await conn.run_sync(lambda _: None)

        # Doing migrations
        async with self._engine.begin() as conn:

            def _do_upgrade(sync_conn):
                self._alembic_cfg.attributes["connection"] = sync_conn
                command.upgrade(self._alembic_cfg, "head")

            await conn.run_sync(_do_upgrade)

    async def disconnect(self) -> None:
        """Method for closing a connection to database."""

        await self._engine.dispose()


database = Database(settings.db_url, settings.DEBUG)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Opens an AsyncSession and guarantees to close it after the request."""
    async with database.get_session() as session:
        yield session
