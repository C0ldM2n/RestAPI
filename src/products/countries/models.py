import typing

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import BaseModel, TimeMixin

if typing.TYPE_CHECKING:
    from products.brands.models import Brand


class Country(BaseModel, TimeMixin):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, nullable=False
    )
    name: Mapped[str]

    brands: Mapped[list["Brand"]] = relationship(back_populates="country")
