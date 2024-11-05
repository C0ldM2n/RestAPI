from .enums import EnumException


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


class DatabaseIntegrityError(CustomException):
	def __init__(self, *args):
		super().__init__(*args, exc_enum=EnumException.DATABASE_INTEGRITY_ERROR)


class UnexpectedError(CustomException):
	def __init__(self, *args):
		super().__init__(*args, exc_enum=EnumException.UNEXPECTED_ERROR)


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
