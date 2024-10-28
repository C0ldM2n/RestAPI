from .exp import (
    ValidationError,
    ValidationQueryError,
    CategoryAlreadyCreated,
    CategoryOnThisLevelAlreadyCreated,
    CategoryNotFounded,
    ProductAlreadyCreated,
)

ValidationExceptions = ["ValidationError", "ValidationQueryError"]

CategoryExceptions = [
    "CategoryAlreadyCreated",
    "CategoryOnThisLevelAlreadyCreated",
    "CategoryNotFounded",
]

ProductExceptions = ["ProductAlreadyCreated"]
