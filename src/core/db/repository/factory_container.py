from dependency_injector import containers, providers

from core.db.repository.repository_factory import RepositoryFactory


class Container(containers.DeclarativeContainer):
    repository_factory = providers.Factory(RepositoryFactory)
