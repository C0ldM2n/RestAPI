import typing

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, DateTimeMixin

if typing.TYPE_CHECKING:
    from brands.models import Brand


class Country(Base, DateTimeMixin):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str]

    brands: Mapped[list["Brand"]] = relationship(back_populates="country")
