from pydantic import BaseModel, Field, conlist


class Response(BaseModel):
    """Generic response model that consist only one result."""

    result: BaseModel


class ResponseMulti(BaseModel):
    """Generic response model that consist multiple results."""

    result: list[BaseModel]


class ErrorResponse(BaseModel):
    """Error response model."""

    message: str = Field(description="This field represent the message")
    path: list = Field(
        description="The path to the field that raised the error",
        default_factory=list,
    )
    detail: dict | str = Field(
        description="The detail of the error", default_factory=str
    )


class ErrorResponseMulti(BaseModel):
    """The public error response model that includes multiple objects."""

    errors: conlist(ErrorResponse, min_length=1)
