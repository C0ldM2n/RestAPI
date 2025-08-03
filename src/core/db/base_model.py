from uuid import UUID

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Basic model for all models."""

    __allow_unmapped__ = True

    id: int | UUID
