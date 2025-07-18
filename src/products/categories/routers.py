from typing import Annotated

from fastapi import APIRouter, Depends, status, Path

from core.db.repository.repository_factory import RepositoryFactory
from models import Category
from products.categories.schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

CategoryID = Annotated[int, Path(..., alias="id")]


@router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreateSchema,
    factory: RepositoryFactory = Depends(RepositoryFactory),
):
    repo = factory(Category)
    new_category = await repo.create(data)
    return new_category


@router.get(
    "/{id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def read_category(
    category_id: CategoryID,
    factory: RepositoryFactory = Depends(RepositoryFactory),
):
    repo = factory(Category)
    category = await repo.read(category_id)
    return category


@router.put(
    "/{id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    category_id: CategoryID,
    data: CategoryUpdateSchema,
    factory: RepositoryFactory = Depends(RepositoryFactory),
):
    repo = factory(Category)
    updated_category = await repo.update(category_id, data)
    return updated_category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: CategoryID,
    factory: RepositoryFactory = Depends(RepositoryFactory),
):
    repo = factory(Category)
    await repo.delete(category_id)
    return
