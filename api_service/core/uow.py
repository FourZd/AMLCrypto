from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from core.logger import logger


class UnitOfWork:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ):
        """
        :param session_factory: Фабрика для создания сессии базы данных
        """
        self.session_factory = session_factory
        self.session: Optional[AsyncSession] = None
        self.transaction = None

    async def begin(self):
        """
        Метод для явного начала транзакции.
        """
        if self.session is None:
            async with self.session_factory() as session:
                self.session = session
                self.transaction = await self.session.begin()

    async def commit(self):
        """
        Коммит транзакции.
        """
        if self.session is None or self.transaction is None:
            raise RuntimeError("Session or transaction not initialized.")

        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error during commit: {e}")
            raise RuntimeError(f"Failed to commit transaction: {e}") from e

    async def rollback(self):
        """
        Откат транзакции.
        """
        if self.session is None or self.transaction is None:
            raise RuntimeError("Session or transaction not initialized.")

        try:
            await self.session.rollback()
        except Exception as e:
            logger.error(f"Error during rollback: {e}")
            raise RuntimeError(f"Failed to rollback transaction: {e}") from e

    async def close(self):
        """
        Завершение работы сессии и транзакции.
        """
        if self.session is not None:
            try:
                await self.session.close()
            except Exception as e:
                logger.error(f"Error during session closing: {e}")
                raise RuntimeError(f"Failed to close session: {e}") from e
            finally:
                self.session = None
                self.transaction = None

    async def get_session(self) -> AsyncSession:
        """
        Возвращает текущую сессию для использования в репозиториях.
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized or already closed.")
        return self.session