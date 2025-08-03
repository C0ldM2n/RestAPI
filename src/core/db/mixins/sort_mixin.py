from sqlalchemy.orm import (
    declarative_mixin,
    mapped_column,
    Mapped,
)


# noinspection PyMethodParameters
@declarative_mixin
class SortMixin:
    """Mixin class to represent a sortable model."""

    sort_order: Mapped[int] = mapped_column(nullable=False)
