from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Path

from products.categories.repository import CategoryRepository
from products.categories.schemas import CategoryCreateSchema, CategoryUpdateSchema, CategoryResponseSchema
from core.exceptions import CategoryAlreadyCreated, \
	CategoryOnThisLevelAlreadyCreated, CategoryNotFounded
from core.exceptions.exp import CategoryUnprocessableEntity

router = APIRouter(
	prefix="/categories",
	tags=["Categories"]
)

CategoryID = Annotated[int, Path(..., alias="id")]
CategoryRepo = Annotated[CategoryRepository, Depends(CategoryRepository.get_category_repository)]

# Add validating errors
# and read abt HTTPException
# (abt convert ex's to HTTPException)

@router.post("/categories/create", response_model=CategoryCreateSchema, status_code=status.HTTP_201_CREATED)
async def create_category(
		data: CategoryCreateSchema,
		category_repo: CategoryRepo
):

	new_category = await category_repo.create(data)
	return new_category

	# except Exception as e:
	# 	err_msg = str(e)
	#
	# 	if '"categories_pkey"' in err_msg:
	# 		raise CategoryAlreadyCreated(data.id, data.name)
	#
	# 	if '"uq_name_parent_id"' in err_msg:
	# 		raise CategoryOnThisLevelAlreadyCreated(data.parent_id, data.name)
	#
	# 	if 'cannot have itself as its parent' in err_msg:
	# 		raise CategoryUnprocessableEntity(data.id, data.parent_id)
	#
	# 	# Handle any unexpected errors and return a 400 status code
	# 	else:
	# 		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
	# 		                    detail="An error occurred while creating the category")


@router.get("/categories/get/{id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
async def get_category_by_id(
		category_id: CategoryID,
		category_repo: CategoryRepo
):

	category = await category_repo.get_by_id(category_id)
	return category

	# except Exception as e:
	# 	err_msg = str(e)
	# 	# Handle any unexpected errors and return a 400 status code
	# 	print(f"Error {err_msg}")
	# 	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
	# 	                    detail="An error occurred while getting the category")


@router.put("/categories/update/{id}", response_model=CategoryUpdateSchema, status_code=status.HTTP_200_OK)
async def update_category(
		category_id: CategoryID,
		data: CategoryUpdateSchema,
		category_repo: CategoryRepo
):

	try:
		category_updated = await category_repo.put(category_id, data)
		return category_updated

	except Exception as e:
		err_msg = str(e)

		if 'cannot have itself as its parent' in err_msg:
			raise CategoryUnprocessableEntity(data.id, data.parent_id)

		if 'Item not found' in err_msg:
			raise CategoryNotFounded(category_id)

		# Handle any unexpected errors and return a 400 status code
		else:
			print(f"Error {err_msg}")
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
			                    detail="An error occurred while updating the category")


@router.delete("/categories/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_category_by_id(
		category_id: CategoryID,
		category_repo: CategoryRepo
):

	try:
		await category_repo.delete_by_id(category_id)
		return {"message": "Category deleted successfully"}

	except Exception as e:
		err_msg = str(e)

		if 'Item not found' in err_msg:
			raise CategoryNotFounded(category_id)

		# Handle any unexpected errors and return a 400 status code
		else:
			print(f"Error {err_msg}")
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
			                    detail="An error occurred while deleting the category")
