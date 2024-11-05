from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from products.categories.routers import router as router_categories
from config import settings
from core.exceptions.handler import exception_handler_setup
# from products.routers import router as router_products

app = FastAPI(
	title=settings.APP_NAME
)


exception_handler_setup(app)

@app.exception_handler(500)
async def internal_server_error(request, exc):
	return JSONResponse(
		content={"message": "Oops, something went wrond. Internal server error",
		         "error_code": "server_error"},
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
	)

app.include_router(router_categories)
# app.include_router(router_products)
