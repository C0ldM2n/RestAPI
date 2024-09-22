from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from config import settings

from products.routers import router as router_products

from core.exceptions.exp import CustomException
from core.exceptions.handler import exception_handler_setup

app = FastAPI(
    title=settings.APP_NAME
)

# @app.exception_handler(CustomException)
# async def custom_exception_handler(request: Request, exc: CustomException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "code": exc.message.split()[0].upper(),
#             "status": exc.status_code,
#             "message": exc.message
#         }
#     )

exception_handler_setup(app)

app.include_router(router_products)
