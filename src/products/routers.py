from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from core.db.database import get_async_session

from products.schemas import ProductPydantic
from products.crud import save_product_to_db, get_product_from_db

router = APIRouter()


@router.post("/", response_model=ProductPydantic)
async def create_product(product: ProductPydantic, session: AsyncSession = Depends(get_async_session)):
    created_product = await save_product_to_db(product, session)
    return created_product


@router.get("/{product_id}", response_model=ProductPydantic)
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    product = await get_product_from_db(product_id, session)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
