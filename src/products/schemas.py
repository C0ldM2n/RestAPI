from typing import Optional

from pydantic import BaseModel, UUID4


class ProductCreate(BaseModel):
    name: str
    brand_id: int
    category_id: int
    price: int
    sku: Optional[str]
    isbn: Optional[str]
    quantity: int
    published: bool
    created_by: Optional[UUID4]
    updated_by: Optional[UUID4]

    class Config:
        from_attributes = True
