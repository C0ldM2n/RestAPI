from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product

async def save_product_to_db(product_data, session: AsyncSession) -> Product:
    new_product = Product(**product_data.dict())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product

async def get_product_from_db(product_id: int, session: AsyncSession) -> Product | None:
    product = await session.get(Product, product_id)
    return product
