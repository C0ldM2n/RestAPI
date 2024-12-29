from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint, Integer, CheckConstraint
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    validates,
    relationship,
    declarative_mixin,
    backref,
)


@declarative_mixin
class HierarchicalMixin:
    """A mixin class to represent hierarchical relationships in a tree structure."""

    __tablename__: str

    @declared_attr
    def rgt(cls) -> Mapped[int]:
        return mapped_column(Integer, nullable=False, index=True)

    @declared_attr
    def lft(cls) -> Mapped[int]:
        return mapped_column(Integer, nullable=False, index=True)

    @declared_attr
    def level(cls) -> Mapped[int]:
        return mapped_column(Integer, nullable=False, index=True)

    @declared_attr
    def parent_id(cls) -> Mapped[Optional[int]]:
        return mapped_column(
            Integer,
            ForeignKey(f"{cls.__tablename__}.id"),
            nullable=True,
            index=True,
        )

    @declared_attr
    def sort_order(cls) -> Mapped[int]:
        return mapped_column(Integer, nullable=False)

    @declared_attr
    def parent(cls) -> Mapped[Optional["HierarchicalMixin"]]:
        return relationship(
            cls,
            remote_side=cls.id,
            backref=backref("children", cascade="all"),
        )

    @declared_attr
    def __table_args__(cls):
        table_args = []

        # Unique constraint for unique name per level
        if hasattr(cls, "name"):
            table_args.append(
                UniqueConstraint(
                    "name", "level", name=f"uq_{cls.__tablename__}_name_level"
                )
            )

        # Unique constraint for unique sort order per level
        table_args.append(
            UniqueConstraint(
                "sort_order",
                "level",
                name=f"uq_{cls.__tablename__}_sort_order_level",
            )
        )

        # TODO: fix
        # Unique constraint for one usage of parent_id = null
        table_args.append(
            CheckConstraint(
                "parent_id IS NULL", name=f"ck_{cls.__tablename__}_single_root"
            )
        )

        return tuple(table_args)

    # TODO: Check for cyclic reference and move to utils
    @validates("parent_id")
    def validate_parent_id(self, key, parent_id):
        """Ensure parent_id does not reference itself as its own parent."""
        # if parent_id == self.id:
        if parent_id is not None and parent_id == f"{self.__tablename__}.id":
            raise ValueError("A node cannot be its ownparent.")
        return parent_id
