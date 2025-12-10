from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase

convention = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseModel(DeclarativeBase):
    """Basic model for all models."""

    __allow_unmapped__ = True

    id: int | UUID

    metadata = MetaData(naming_convention=convention)

    type_annotation_map = {
        datetime: DateTime(timezone=True),
    }
