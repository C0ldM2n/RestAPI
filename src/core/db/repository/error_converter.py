import traceback
from functools import wraps

from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    DatabaseError,
    NotFoundError,
)
from core.exceptions.mapper import MAPPINGS


def convert_db_errors():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                result = await func(self, *args, **kwargs)

                if result is None:
                    pk = args[0] if not isinstance(args[0], dict) else args[0]["id"]
                    detail = "Result = None. Entity not found."
                    raise NotFoundError(pk=pk, detail=detail)

                return result

            except IntegrityError as e:
                detail = str(e.orig)
                for pattern, exc_class, build_kwargs in MAPPINGS:
                    if pattern.search(detail):
                        # print(f"----------\n{detail}")
                        raise exc_class(**build_kwargs(detail))
                raise DatabaseError(detail=detail)

            except Exception as e:
                detail = str(e)
                await self._session.rollback()
                if isinstance(e, NotFoundError):
                    raise
                print(traceback.format_exc())
                raise DatabaseError(detail=detail)

        return wrapper

    return decorator
