from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.db.database import get_async_session
from core.exceptions.exp import ProductAlreadyCreated

from core.cli import bulk_insert_data_from_files

from models import Product, Category, Brand
from products.schemas import ProductCreate
from products.crud import save_product_to_db, get_product_from_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductCreate, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        created_product = await save_product_to_db(product, session)
    # TODO: handling errors
    except IntegrityError as e:
        err_msg = e.args[0]
        print(err_msg)
        raise ProductAlreadyCreated(product.isbn, product.sku)

    return created_product


@router.get("/{product_id}", response_model=ProductCreate)
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    product = await get_product_from_db(product_id, session)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/bulk-create-products", response_model=list[ProductCreate], status_code=status.HTTP_201_CREATED)
async def bulk_create_products(product: list[ProductCreate], session: AsyncSession = Depends(get_async_session)):
    created_products = [Product(**product.model_dump()) for product in product]
    session.add_all(created_products)
    await session.commit()

    for created_product in created_products:
        await session.refresh(created_product)
    #     print(f"===============Product added with ID: {created_product.id}===============")
    # print(created_products)

    return [ProductCreate.model_validate(created_product) for created_product in created_products]


@router.post("/bulk-fill-tables", status_code=status.HTTP_201_CREATED)
async def bulk_fill_tables(files: list[UploadFile] = File(...), session: AsyncSession = Depends(get_async_session)):
    """
    Bulk insert data into tables from uploaded JSON files.
    """
    file_paths = []

    # Save the uploaded files to a temporary location
    for file in files:
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="Only JSON files are allowed.")

        temp_file_path = Path(f"/tmp/{file.filename}")  # Use a temporary directory
        with temp_file_path.open("wb") as buffer:
            buffer.write(await file.read())
        file_paths.append(temp_file_path)

    try:
        await bulk_insert_data_from_files(file_paths, session)
        await session.commit()
        return {"message": "Data inserted successfully."}
    except Exception as e:
        print(f"Error during bulk insertion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear-all", status_code=204)
async def clear_all_records(session: AsyncSession = Depends(get_async_session)):
    """
    Delete all records from all tables.
    """
    try:
        await session.execute(delete(Product))
        await session.execute(delete(Category))
        await session.execute(delete(Brand))

        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "All records deleted successfully."}
