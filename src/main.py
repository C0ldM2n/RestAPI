import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from products.categories.routers import router as router_categories
from config import settings
from core.exceptions.handler import setup_exception_handlers

app = FastAPI(title=settings.APP_NAME)

# SQLAlchemy logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


setup_exception_handlers(app)

# @app.exception_handler(500)
# async def internal_server_error(request, exc):
# 	return JSONResponse(
# 		content={"message": "Oops, something went wrong. Internal server error",
# 		         "error_code": "server_error"},
# 		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# 	)

app.include_router(router_categories)
