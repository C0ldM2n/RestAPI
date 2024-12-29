from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status

from .base import BaseError
from .response import ErrorResponseMulti, ErrorResponse


def setup_exception_handlers(app):
    """Setup exception handlers."""
    app.add_exception_handler(BaseError, custom_base_errors_handler)
    app.add_exception_handler(Exception, python_base_error_handler)
    app.add_exception_handler(
        RequestValidationError, pydantic_validation_errors_handler
    )


def custom_base_errors_handler(_: Request, error: BaseError) -> JSONResponse:
    """This function is called if the BaseError was raised."""

    response = ErrorResponseMulti(
        errors=[ErrorResponse(message=error.message, detail=error.detail)]
    )

    return JSONResponse(
        response.model_dump(by_alias=True),
        status_code=error.status_code,
    )


def python_base_error_handler(_: Request, error: Exception) -> JSONResponse:
    """This function is called if the Exception was raised."""

    response = ErrorResponseMulti(
        errors=[
            ErrorResponse(
                message=f"An unexpected error occurred.", detail=str(error)
            )
        ]
    )

    return JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def pydantic_validation_errors_handler(
    _: Request, error: RequestValidationError
) -> JSONResponse:
    """This function is called if the Pydantic validation error was raised."""

    response = ErrorResponseMulti(
        errors=[
            ErrorResponse(
                message=err["msg"],
                path=list(err["loc"]),
            )
            for err in error.errors()
        ]
    )

    return JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
