import enum


class EnumException(enum.Enum):
    VALIDATION_ERROR = "Validation error in the request body.", 422
    VALIDATION_QUERY_ERROR = "Validation error in the request query.", 422

    CATEGORY_ALREADY_CREATED = (
        "Category with name = {1} already created. Problem with field id = {0}.",
        409,
    )
    CATEGORY_ON_THIS_LEVEL_ALREADY_CREATED = (
        "Category with name = {1} on this level"
        " already created. Problem with field parent_id = {0} and name = {1}."
    ), 409

    CATEGORY_NOT_FOUNDED = "Category with id {0} not founded.", 404

    CATEGORY_UNPROCESSABLE_ENTITY = (
        "Category tries to set a category as its own parent. parent_id = {1} same that id = {0}",
        422,
    )

    PRODUCT_ALREADY_CREATED = (
        "Product with name {0} already created. Problem with field {1}.",
        403,
    )
