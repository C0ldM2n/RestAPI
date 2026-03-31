from core.db.repository.interfaces import IRepository


class RouterFactory:
    def __init__(
        self,
        repository: IRepository,
    ) -> None:
        self.repository = repository
