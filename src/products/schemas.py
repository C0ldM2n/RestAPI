from pydantic import BaseModel

class ProductPydantic(BaseModel):
    name: str
    price: int
    sku: str
    isbn: str
    quantity: int
    published: bool
    created_by: str
    updated_by: str
