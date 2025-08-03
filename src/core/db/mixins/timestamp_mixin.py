from sqlalchemy import DateTime, func
from sqlalchemy.orm import (
    declarative_mixin,
    mapped_column,
    Mapped,
)


# noinspection PyMethodParameters
@declarative_mixin
class TimestampMixin:
    """"""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
