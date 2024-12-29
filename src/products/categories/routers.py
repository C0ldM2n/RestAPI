from typing import Annotated

from fastapi import APIRouter, Depends, status, Path

from products.categories.repository import CategoryRepository
from products.categories.schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

CategoryID = Annotated[int, Path(..., alias="id")]  # why we use this?
CategoryRepo = Annotated[
    CategoryRepository, Depends(CategoryRepository.get_category_repository)
]


@router.post(
    "/create",
    response_model=CategoryCreateSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreateSchema, category_repo: CategoryRepo
):

    new_category = await category_repo.create_node(data.model_dump())
    return new_category


@router.get(
    "/get/{id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    category_id: CategoryID, category_repo: CategoryRepo
):

    category = await category_repo.get_by_id(category_id)
    return category


# ----- not ready -----


@router.put(
    "/update/{id}",
    response_model=CategoryUpdateSchema,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    category_id: CategoryID,
    data: CategoryUpdateSchema,
    category_repo: CategoryRepo,
):

    try:
        category_updated = await category_repo.put(
            category_id, data.model_dump()
        )
        return category_updated

    except Exception as e:
        err_msg = str(e)

        if "cannot have itself as its parent" in err_msg:
            raise CategoryUnprocessableEntity(data.id, data.parent_id)

        if "Item not found" in err_msg:
            raise CategoryNotFounded(category_id)

        # Handle any unexpected errors and return a 400 status code
        else:
            print(f"Error {err_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An error occurred while updating the category",
            )


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_category_by_id(
    category_id: CategoryID, category_repo: CategoryRepo
):

    try:
        await category_repo.delete_by_id(category_id)
        return {"message": "Category deleted successfully"}

    except Exception as e:
        err_msg = str(e)

        if "Item not found" in err_msg:
            raise CategoryNotFounded(category_id)

        # Handle any unexpected errors and return a 400 status code
        else:
            print(f"Error {err_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An error occurred while deleting the category",
            )
