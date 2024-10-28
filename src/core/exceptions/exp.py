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


#     Add exceptions for put and patch


class CustomException(Exception):
    def __init__(self, *args, exc_enum=None, headers=None):
        if exc_enum is None or not isinstance(exc_enum, EnumException):
            raise ValueError("Invalid exception type or not provided")
        self.code = exc_enum.name
        # TODO: create check count variable arguments
        self.message = exc_enum.value[0].format(*args)
        self.status_code = exc_enum.value[1]
        self.headers = headers


class ValidationError(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.VALIDATION_ERROR)


class ValidationQueryError(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.VALIDATION_QUERY_ERROR)


class CategoryAlreadyCreated(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.CATEGORY_ALREADY_CREATED)


class CategoryOnThisLevelAlreadyCreated(CustomException):
    def __init__(self, *args):
        super().__init__(
            *args, exc_enum=EnumException.CATEGORY_ON_THIS_LEVEL_ALREADY_CREATED
        )


class CategoryNotFounded(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.CATEGORY_NOT_FOUNDED)


class CategoryUnprocessableEntity(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.CATEGORY_UNPROCESSABLE_ENTITY)


class ProductAlreadyCreated(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.PRODUCT_ALREADY_CREATED)
