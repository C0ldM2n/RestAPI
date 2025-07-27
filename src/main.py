from fastapi import FastAPI

from config import settings
from core.logger import setup_logger
from core.middleware.error_middleware import ErrorMiddleware
from products.categories.routers import router as router_categories

setup_logger()

app = FastAPI(title=settings.APP_NAME)


app.add_middleware(ErrorMiddleware)

app.include_router(router_categories)
