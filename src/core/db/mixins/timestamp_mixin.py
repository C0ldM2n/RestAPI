from sqlalchemy import DateTime, func
from sqlalchemy.orm import declarative_mixin, mapped_column, declared_attr, Mapped


# noinspection PyMethodParameters
@declarative_mixin
class TimestampMixin:

    @declared_attr
    def created_at(cls) -> Mapped[DateTime]:
        return mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )

    @declared_attr
    def updated_at(cls) -> Mapped[DateTime]:
        return mapped_column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
