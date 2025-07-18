from uuid import UUID

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __allow_unmapped__ = True

    id: int | UUID
