from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    declared_attr,
    mapped_column,
)

from core.db.mixins.sort_mixin import SortMixin


# noinspection PyMethodParameters
@declarative_mixin
class TreeMixin(SortMixin):
    """A mixin class to represent hierarchical relationships in a tree structure."""

    __tablename__: str

    @declared_attr
    def parent_id(cls) -> Mapped[int | None]:
        return mapped_column(
            ForeignKey(f"{cls.__tablename__}.id", ondelete="CASCADE"),
            nullable=True,
            index=True,
        )
