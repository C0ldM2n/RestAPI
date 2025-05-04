from fastapi import APIRouter


class BaseTestAPI:
    def __init__(self, router: APIRouter):
        self.api = router
