import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from users.models import User


class UserMixin:
    # created_by: Mapped[str] = mapped_column(ForeignKey("users.name"),
    #                                         nullable=True  # dev
    #                                         )
    # updated_by: Mapped[str] = mapped_column(ForeignKey("users.name"),
    #                                         nullable=True  # dev
    #                                         )

    created_by: Mapped[str] = mapped_column(nullable=True)
    updated_by: Mapped[str] = mapped_column(nullable=True)

    # users: Mapped["User"] = relationship(back_populates="category")
