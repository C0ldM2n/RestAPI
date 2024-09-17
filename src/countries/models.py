from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)

    brands: Mapped[list["Brand"]] = relationship(back_populates="country")
