from typing import Annotated

from fastapi import APIRouter, Depends, status, Path

from products.categories.repository import CategoryRepository
from products.categories.schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

CategoryID = Annotated[int, Path(..., alias="id")]
CategoryRepo = Annotated[
    CategoryRepository, Depends(CategoryRepository.get_category_repository)
]


@router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
        data: CategoryCreateSchema, category_repo: CategoryRepo
):
    new_category = await category_repo.create(data)
    return new_category


@router.get(
    "/{id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_category(
        category_id: CategoryID, category_repo: CategoryRepo
):
    category = await category_repo.read(category_id)
    return category


@router.put(
    "/{id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_category(
        category_id: CategoryID,
        data: CategoryUpdateSchema,
        category_repo: CategoryRepo,
):
    updated_category = await category_repo.update(category_id, data)
    return updated_category


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
        category_id: CategoryID, category_repo: CategoryRepo
):
    await category_repo.delete(category_id)
    return
