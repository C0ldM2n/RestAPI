from fastapi import FastAPI

from config import settings

from products.routers import router as router_products

from core.exceptions.handler import exception_handler_setup

app = FastAPI(
    title=settings.APP_NAME
)


exception_handler_setup(app)

app.include_router(router_products)
