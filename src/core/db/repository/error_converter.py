import traceback
from functools import wraps

from loguru import logger
from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    DatabaseError,
    NotFoundError,
)
from core.exceptions.mapper import MAPPINGS
from core.exceptions.base import CyclicReferenceError


def convert_db_errors():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                # Execute the function and handle the result
                result = await func(self, *args, **kwargs)

                # If the function is expected to return a result, check if it's None
                if result is None:
                    pk = args[0]
                    raise NotFoundError(pk=pk)

                return result

            # Handle specific database errors
            except IntegrityError as e:
                detail = str(e.orig)
                for pattern, exc_class, build_kwargs in MAPPINGS:
                    if pattern.search(detail):
                        logger.debug(f"----------\n{detail}")
                        raise exc_class(**build_kwargs(detail))

                raise DatabaseError(detail=detail)

            # Handle other exceptions
            except Exception as e:
                detail = str(e)
                await self._session.rollback()

                if isinstance(
                    e,
                    (
                        NotFoundError,
                        CyclicReferenceError,
                    ),
                ):
                    raise
                logger.error(
                    f"Unhandled exception in {func.__name__}: "
                    f"{traceback.format_exc()}"
                )

                raise DatabaseError(detail=detail)

        return wrapper

    return decorator
