import typing

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base

if typing.TYPE_CHECKING:
    from products.models import Product
    from countries.models import Country


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country_registration_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    name: Mapped[str] = mapped_column(String)

    products: Mapped[list["Product"]] = relationship(back_populates="brand")
    country: Mapped["Country"] = relationship(back_populates="brands")
