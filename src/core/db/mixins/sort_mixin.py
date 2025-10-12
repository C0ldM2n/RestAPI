from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    mapped_column,
)


# noinspection PyMethodParameters
@declarative_mixin
class SortMixin:
    """Mixin class to represent a sortable model."""

    sort_order: Mapped[int] = mapped_column(nullable=False)
