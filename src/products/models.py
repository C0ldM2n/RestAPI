import uuid

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, DateTimeMixin

from brands.models import Brand
from categories.models import Category


class Product(Base, DateTimeMixin):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,
                                     nullable=False, index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str]
    price: Mapped[int]
    sku: Mapped[str] = mapped_column(String, nullable=True)
    isbn: Mapped[str] = mapped_column(String, nullable=True)
    quantity: Mapped[int]
    published: Mapped[bool]
    created_by: Mapped[UUID] = mapped_column(UUID, nullable=True)
    updated_by: Mapped[UUID] = mapped_column(UUID, nullable=True)

    brand: Mapped["Brand"] = relationship(back_populates="products")
    category: Mapped["Category"] = relationship(back_populates="products")
