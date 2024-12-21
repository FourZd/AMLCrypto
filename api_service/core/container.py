from dependency_injector import containers, providers
from core.database import Database
from core.environment import env
from transactions.repositories import TransactionRepository
from transactions.services import TransactionService


class Container(containers.DeclarativeContainer):
    """
    DI container for the application resources.
    Using dependency_injector library.
    """
    wiring_config = containers.WiringConfiguration(
        modules=[
            "transactions.router",
        ]
    )

    db = providers.Singleton(
        Database,
        db_url=f"{env.DATABASE_DIALECT}+asyncpg://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}@{env.POSTGRES_HOSTNAME}:{env.POSTGRES_PORT}/{env.POSTGRES_DB}",
    )

    transaction_repository = providers.Factory(
        TransactionRepository,
        session_factory=db.provided.session,
    )

    transaction_service = providers.Factory(
        TransactionService,
        transaction_repository=transaction_repository,
    )
    

