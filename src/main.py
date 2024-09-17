from fastapi import FastAPI

from config import settings

from products.routers import router as router_products


app = FastAPI(
    title=settings.APP_NAME
)

app.include_router(router_products)
