import enum


class EnumException(enum.Enum):
    VALIDATION_ERROR = 'Validation error in the request body.', 422
    VALIDATION_QUERY_ERROR = 'Validation error in the request query.', 422

    USER_NOT_FOUND = 'User not found.', 404
    USER_ALREADY_EXISTS = 'User {0} already exists.', 400
    EMAIL_ALREADY_EXISTS = 'Email {0} already exists.', 400
    NOT_VALID_EMAIL = 'Email {0} is not valid.', 400
    EMAIL_DOES_NOT_EXIST = 'Email {0} does not exist.', 400
    AUTHENTICATION_ERROR = 'Authentication error.', 401
    UNAUTHORIZED = 'Unauthorized.', 401

    INVALID_AUTHORIZATION_CODE = "Invalid authorization code.", 403
    INVALID_JWT_TOKEN_EXPIRED = "Invalid token or expired token.", 403
    INVALID_AUTHENTICATION_SCHEME = "Invalid authentication scheme, {0} ", 403

    INVALID_API_KEY = "Invalid API key.", 403
    API_TOKEN_ALREADY_EXISTS = 'Token with this name already exists.', 400
    FOLLOW_MESSAGE_NOT_FOUND = 'Follow message not found.', 404
    USER_ALREADY_SUBSCRIBED = 'User already subscribed.', 400
    FEEDBACK_ALREADY_EXISTS = 'Feedback already exists.', 400


class CustomException(Exception):
    def __init__(self, *args, exc_enum=None, headers=None):
        if exc_enum is None or not isinstance(exc_enum, EnumException):
            raise ValueError('Invalid exception type or not provided')
        self.code = exc_enum.name
        self.message = exc_enum.value[0].format(*args)
        self.status_code = exc_enum.value[1]
        self.headers = headers



class ValidationError(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.VALIDATION_ERROR)


class ValidationQueryError(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.VALIDATION_QUERY_ERROR)



class UserNotFound(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.USER_NOT_FOUND)


class UserAlreadyExists(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.USER_ALREADY_EXISTS)


class EmailAlreadyExists(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.EMAIL_ALREADY_EXISTS)


class NotValidEmail(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.NOT_VALID_EMAIL)


class EmailDoesNotExists(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.EMAIL_DOES_NOT_EXIST)


class AuthenticationError(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.AUTHENTICATION_ERROR)


class Unauthorized(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.UNAUTHORIZED)



class InvalidAuthorizationCode(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.INVALID_AUTHORIZATION_CODE)


class InvalidJWTTokenExpired(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.INVALID_JWT_TOKEN_EXPIRED)


class InvalidAuthenticationScheme(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.INVALID_AUTHENTICATION_SCHEME)



class InvalidAPIKey(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.INVALID_API_KEY)


class APITokenAlreadyExists(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.API_TOKEN_ALREADY_EXISTS)


class FollowMessageNotFound(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.FOLLOW_MESSAGE_NOT_FOUND)


class UserAlreadySubscribed(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.USER_ALREADY_SUBSCRIBED)


class FeedbackAlreadyExists(CustomException):
    def __init__(self, *args):
        super().__init__(*args, exc_enum=EnumException.FEEDBACK_ALREADY_EXISTS)
