from fastapi import FastAPI

from products.categories.routers import router as router_categories
from config import settings
from core.exceptions.handler import exception_handler_setup
# from products.routers import router as router_products

app = FastAPI(
    title=settings.APP_NAME
)


exception_handler_setup(app)

app.include_router(router_categories)
# app.include_router(router_products)
