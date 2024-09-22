from sqlalchemy.ext.asyncio import AsyncSession

from products.models import Product


async def save_product_to_db(product_data, session: AsyncSession) -> Product:
    new_product = Product(**product_data.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    # test
    print(f"Product added with ID: {new_product.id}")
    return new_product


async def get_product_from_db(product_id: int, session: AsyncSession) -> Product | None:
    product = await session.get(Product, str(product_id))
    print(product)
    return product
