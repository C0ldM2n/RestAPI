import uuid

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __allow_unmapped__ = True

    id: int | uuid.UUID
