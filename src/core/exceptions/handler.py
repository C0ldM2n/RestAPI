from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import IntegrityError
from starlette import status

from core.exceptions.base import BaseError, DatabaseError
from core.exceptions.mapper import MAPPINGS
from core.exceptions.schemas import ApiError, ApiErrorResponse, ErrorCode


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Sets exception handlers for:
        Pydantic validation errors
        SQLAlchemy integrity errors
        Custom errors
        Python errors
    """

    app.add_exception_handler(
        RequestValidationError,
        pydantic_validation_errors_handler,
    )
    app.add_exception_handler(
        IntegrityError,
        sqlalchemy_integrity_errors_handler,
    )
    app.add_exception_handler(
        BaseError,
        api_errors_handler,
    )
    app.add_exception_handler(
        Exception,
        python_generic_error_handler,
    )


def api_errors_handler(_: Request, error: BaseError) -> JSONResponse:
    """
    This function is called if the BaseError was raised.
    Works for errors thrown from business logic.
    """

    response = ApiErrorResponse(
        errors=[
            ApiError(
                code=error.code,
                message=error.message,
                path=error.path,
            )
        ]
    )

    return JSONResponse(
        response.model_dump(by_alias=True),
        status_code=error.status_code,
    )


def sqlalchemy_integrity_errors_handler(
    _: Request, error: IntegrityError
) -> JSONResponse:
    """
    This function is called when an SQLAlchemy IntegrityError occurs.
    An exception that occurs when relational database integrity is violated.
    """
    logger.error(f"IntegrityError occurred: {error.orig}")

    detail = str(error.orig)
    custom_error = None

    for pattern, exc_class, parser_func in MAPPINGS:
        if pattern.search(detail):
            if parsed_args := parser_func(detail):
                # Create a custom error instance with parsed data
                custom_error = exc_class(**parsed_args)
                break

    # If we couldn't identify the error, we use a general database error
    final_error = custom_error or DatabaseError()

    response = ApiErrorResponse(
        errors=[
            ApiError(
                code=final_error.code,
                message=final_error.message,
                path=final_error.path,
            )
        ]
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=custom_error.status_code,
    )


def pydantic_validation_errors_handler(
    _: Request, error: RequestValidationError
) -> JSONResponse:
    """This function is called if the Pydantic validation error was raised."""

    response = ApiErrorResponse(
        errors=[
            ApiError(
                code=ErrorCode.VALIDATION_ERROR,
                message=err["msg"],
                path=err["loc"][1:],
            )
            for err in error.errors()
        ]
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def python_generic_error_handler(_: Request, error: Exception) -> JSONResponse:
    """This function is called if the Python Exception was raised."""

    logger.exception(f"An unexpected error occurred: {error}")

    response = ApiErrorResponse(
        errors=[
            ApiError(
                code=ErrorCode.UNEXPECTED_ERROR,
                message="An unexpected error occurred on the server.",
            )
        ]
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
