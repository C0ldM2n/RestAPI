from typing import Annotated

from fastapi import APIRouter, status, Path

from products.categories.schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)
from products.categories.dependencies import (
    CategoryFromPath,
    CategoryRepositoryDep,
)


router = APIRouter(prefix="/categories", tags=["Categories"])

CategoryID = Annotated[int, Path(..., alias="id", gt=0)]


@router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreateSchema,
    repository: CategoryRepositoryDep,
):
    new_category = await repository.create(data)
    return new_category


@router.get(
    "/{id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def read_category(
    category: CategoryFromPath,
):
    return category


@router.put(
    "/{id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    category: CategoryFromPath,
    data: CategoryUpdateSchema,
    repository: CategoryRepositoryDep,
):
    updated_category = await repository.update(category.id, data)
    return updated_category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: CategoryID,
    reposotory: CategoryRepositoryDep,
):
    await reposotory.delete(category_id)
    return None
