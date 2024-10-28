
# CategoryRepository: BaseRepository()
#
# def get_repository(session: AsyncSession = Depends(get_async_session)):
#     # CrudFactory(Category, session)
#     global CategoryRepository
#     if CategoryRepository is None:
#         CategoryRepository = CrudFactory(Category, session)
#     return CategoryRepository
#
# CategoryID = Annotated[int, Path(..., alias="id")]
#
# @router.post("/categories/create", response_model=CategoryCreate, status_code=status.HTTP_201_CREATED)
# async def create_category(data: dict, session: AsyncSession = Depends(get_async_session)):
#     # CategoryRepository(session)
#     await CategoryRepository.create(data)
#     return {"message": "Category created"}
#
# @router.get("/categories/get/{id}", response_model=CategoryCreate)
# async def get_categories(category_id: CategoryID, session: AsyncSession = Depends(get_async_session)):
#     # category_repo = CategoryRepository(session)
#     category = await CategoryRepository.get(category_id)
#     if category is None:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return category