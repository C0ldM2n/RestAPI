from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
    declarative_mixin,
    backref,
)

from .sort_mixin import SortMixin


@declarative_mixin
class TreeMixin(SortMixin):
    """A mixin class to represent hierarchical relationships in a tree structure."""

    __tablename__: str

    @declared_attr
    def parent_id(cls) -> Mapped[Optional[int]]:
        return mapped_column(
            Integer,
            ForeignKey(f"{cls.__tablename__}.id", ondelete="CASCADE"),
            nullable=True,
            index=True,
        )

    @declared_attr
    def parent(cls) -> Mapped[Optional["TreeMixin"]]:
        return relationship(
            cls,
            remote_side=[cls.id],
            backref=backref("children", cascade="all"),
            foreign_keys=[cls.parent_id],
        )
