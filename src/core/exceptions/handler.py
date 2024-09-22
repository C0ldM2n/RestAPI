from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from loguru import logger

from .exp import CustomException, EnumException


def exception_handler_setup(app: FastAPI):
    @app.exception_handler(CustomException)
    async def validation_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "status": exc.status_code,
            },
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_request_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()

        if request.method == 'GET':
            exception = EnumException.VALIDATION_QUERY_ERROR
        else:
            exception = EnumException.VALIDATION_ERROR

        # Log the full request for more insight
        logger.error(f"Validation error at: {request.url}")
        logger.error(f"Request body: {await request.body()}")
        logger.error(f"Errors: {errors}")

        response_content = {
            "code": exception.name,
            "message": exception.value[0],
            "details": errors,
            "status": exception.value[1],
        }

        logger.error(response_content)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(response_content),
        )
