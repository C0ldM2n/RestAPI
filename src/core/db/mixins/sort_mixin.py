from sqlalchemy import Integer
from sqlalchemy.orm import declarative_mixin, declared_attr, mapped_column, Mapped


# noinspection PyMethodParameters
@declarative_mixin
class SortMixin:
    """Mixin class to represent a sortable model."""

    @declared_attr
    def sort_order(cls) -> Mapped[int]:
        return mapped_column(Integer, nullable=False)
