from sqlalchemy import Integer
from sqlalchemy.orm import declarative_mixin, declared_attr, mapped_column


@declarative_mixin
class SortMixin:
    """Mixin class to represent a sortable model."""

    @declared_attr
    def sort_order(cls):
        return mapped_column(Integer, nullable=False)
