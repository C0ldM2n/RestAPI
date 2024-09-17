from fastapi import APIRouter, Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_async_session

from products.models import Product
from brands.models import Brand
from products.schemas import ProductPydantic
from products.crud import save_product_to_db, get_product_from_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# @router.get("/get_products")
# async def get_products(session: AsyncSession = Depends(get_async_session)):
#     query = select(Product)
#
#     # print(session)
#     print(query)
#     execute = await session.execute(query)
#
#     result = execute.scalars().all()
#     return result
#
#
# @router.get("/get_products_by_brand/{brand_name}")
# async def get_products_by_brand(brand_name: str = None, session: AsyncSession = Depends(get_async_session)):
#     query = (select(Product.id, Product.name, Product.price, Brand.name.label('brand'))
#              .join(Brand, Product.brand_id == Brand.id)) # noqa
#
#     if brand_name:
#         query = query.where(Brand.name == brand_name)
#
#     print(query)
#     execute = await session.execute(query)
#
#     result = execute.fetchall()
#     return [
#         {
#             "id": row[0],
#             "name": row[1],
#             "price": row[2],
#             "brand": row[3]
#         }
#         for row in result
#     ]


# for tests
from fastapi import HTTPException

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
