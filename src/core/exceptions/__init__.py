from .exp import (
    ValidationError,
    ValidationQueryError,
    DatabaseIntegrityError,
    UnexpectedError,
    CategoryAlreadyCreated,
    CategoryOnThisLevelAlreadyCreated,
    CategoryUnprocessableEntity,
    CategoryNotFounded,
    ProductAlreadyCreated,
)

ValidationExceptions = ["ValidationError", "ValidationQueryError"]

CategoryExceptions = [
    "CategoryAlreadyCreated",
    "CategoryOnThisLevelAlreadyCreated",
    "CategoryNotFounded",
    "CategoryUnprocessableEntity"
]

__all__ = [
    "ValidationError",
    "ValidationQueryError",
    "DatabaseIntegrityError",
    "UnexpectedError",
    "CategoryAlreadyCreated",
    "CategoryOnThisLevelAlreadyCreated",
    "CategoryUnprocessableEntity",
    "CategoryNotFounded"
]

ProductExceptions = ["ProductAlreadyCreated"]
