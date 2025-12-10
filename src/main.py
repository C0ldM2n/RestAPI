from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from core.db import database
from core.exceptions.handler import setup_exception_handlers
from core.logger import setup_logger
from products.categories.routers import router as router_categories

setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await database.connect()

    yield

    await database.disconnect()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

setup_exception_handlers(app)
app.include_router(router_categories)
