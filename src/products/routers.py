from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.db.database import get_async_session

from models import Product

from products.schemas import ProductCreate
from products.crud import save_product_to_db, get_product_from_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/test", response_model=ProductCreate, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    # stmt = insert(Product).values(**product.model_dump())

    # new_product = Product(**product.model_dump())
    # session.add(new_product)
    # await session.commit()
    # await session.refresh(new_product)
    #
    # print(f"Product added with ID: {new_product.id}")


    existing_product = await session.execute(
        select(Product).where(
            (Product.isbn == product.isbn) | (Product.sku == product.sku)
        )
    )
    existing_product = existing_product.scalars().first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail=f"Product with this ISBN or SKU already exists"
        )

    new_product = Product(**product.model_dump())

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    print(f"Product added with ID: {new_product.id}")

    return new_product


@router.post("/", response_model=ProductCreate, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    created_product = await save_product_to_db(product, session)
    return created_product


@router.get("/{product_id}", response_model=ProductCreate)
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    product = await get_product_from_db(product_id, session)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/bulk_create_products", response_model=list[ProductCreate], status_code=status.HTTP_201_CREATED)
async def bulk_create_products(product: list[ProductCreate], session: AsyncSession = Depends(get_async_session)):
    created_products = [Product(**product.model_dump()) for product in product]
    session.add_all(created_products)
    await session.commit()

    for created_product in created_products:
        await session.refresh(created_product)
        print(f"===============Product added with ID: {created_product.id}===============")
    print(created_products)

    return [ProductCreate.from_orm(created_product) for created_product in created_products] # noqa

