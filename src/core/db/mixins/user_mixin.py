import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_mixin, mapped_column, declared_attr, relationship, Mapped

if typing.TYPE_CHECKING:
    from users.models import User


# noinspection PyMethodParameters
@declarative_mixin
class UserMixin:
    # created_by: Mapped[str] = mapped_column(ForeignKey("users.name"),
    #                                         nullable=True  # dev
    #                                         )
    # updated_by: Mapped[str] = mapped_column(ForeignKey("users.name"),
    #                                         nullable=True  # dev
    #                                         )

    @declared_attr
    def created_by(cls) -> Mapped[str]:
        return mapped_column(nullable=True)

    @declared_attr
    def updated_by(cls) -> Mapped[str]:
        return mapped_column(nullable=True)

    # users: Mapped["User"] = relationship(back_populates="category")
