import enum


class EnumException(enum.Enum):
    VALIDATION_ERROR = 'Validation error in the request body.', 422
    VALIDATION_QUERY_ERROR = 'Validation error in the request query.', 422

    PRODUCT_ALREADY_CREATED = 'Product with name {0} already created. Problem with field {1}.', 400


class CustomException(Exception):
    def __init__(self, *args, exc_enum=None, headers=None):
        if exc_enum is None or not isinstance(exc_enum, EnumException):
            raise ValueError('Invalid exception type or not provided')
        self.code = exc_enum.name
        # TODO: create check count variable arguments
        self.message = exc_enum.value[0].format(*args)
        self.status_code = exc_enum.value[1]
        self.headers = headers

# TODO: How to remove def __ini_... (dupl code)

class ValidationError(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.VALIDATION_ERROR)


class ValidationQueryError(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.VALIDATION_QUERY_ERROR)



class ProductAlreadyCreated(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.PRODUCT_ALREADY_CREATED)
