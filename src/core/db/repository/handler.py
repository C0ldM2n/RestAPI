from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    DatabaseError,
    ValidationError,
    AlreadyExistOnThisLevelError,
    NotFoundError,
    UniqueRootError,
)


def handling_repository_errors(func):
    """Decorator for handling repository errors."""

    async def wrapper(self, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            if result is None:
                raise NotFoundError(pk=args[0])
            return result

        except IntegrityError as e:
            # Database integrity error handling
            await self.session.rollback()
            print(e)
            if "parent_id=null already exists" in str(e.args[0]):
                raise UniqueRootError(detail=str(e.args[0]))
            elif (
                'duplicate key value violates unique constraint "uq_categories_name_level"'
                in str(e.args[0])
            ):
                raise AlreadyExistOnThisLevelError(
                    field="name", data=args[0]["name"], detail=str(e.args[0])
                )
            elif (
                'duplicate key value violates unique constraint "uq_categories_sort_order_level"'
                in str(e.args[0])
            ):
                raise AlreadyExistOnThisLevelError(
                    field="sort_order",
                    data=args[0]["sort_order"],
                    detail=str(e.args[0]),
                )

            else:
                raise DatabaseError(detail=str(e.args[0]))

        except ValueError as e:
            # Validating values error handling
            print(10 * "---ValueError---")
            print(e)
            raise DatabaseError(detail=str(e.args[0]))

        except Exception as e:
            # Generic error handling
            await self.session.rollback()
            print(10 * "---Exception---")
            print(e)
            if "not found" in str(e.args[0]):
                # print(args)
                # print(kwargs)
                raise NotFoundError(pk=args[0], detail=str(e.args[0]))

            else:
                raise DatabaseError(detail=str(e.args[0]))

    return wrapper
