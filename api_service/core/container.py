from dependency_injector import containers, providers
from core.database import Database
from core.uow import UnitOfWork
from core.environment import env
from core.redis_client import RedisPool


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[

        ]
    )

    db = providers.Singleton(
        Database,
        db_url=f"{env.DATABASE_DIALECT}+asyncpg://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}@{env.POSTGRES_HOSTNAME}:{env.POSTGRES_PORT}/{env.POSTGRES_DB}",
    )

    unit_of_work = providers.Factory(UnitOfWork, session_factory=db.provided.session)

    redis_pool = providers.Singleton(
        RedisPool,
        redis_url=f"redis://:{env.REDIS_PASSWORD}@{env.REDIS_HOST}:{env.REDIS_PORT}/{env.REDIS_DB}",
    )



