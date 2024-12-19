from web3 import AsyncWeb3
from web3.providers.persistent import (
    WebSocketProvider,
)
import aiohttp
from message_broker import MessageBroker


class TransactionObserver:

    def __init__(self, provider_url: str, message_broker: MessageBroker):
        self.provider = AsyncWeb3(WebSocketProvider(provider_url))
        self.message_broker = message_broker

    async def handle_transaction(self, transaction_hash: str):
        """ Обрабатывает транзакцию по её хэшу """
        try:
            transaction = await self.provider.eth.get_transaction(transaction_hash)
            await self.message_broker.send_transaction(transaction)
        except Exception as e:
            print(f"Error handling transaction {transaction_hash}: {e}")

    async def observe(self):
        """ Асинхронный метод для наблюдения за новыми транзакциями """
        subscription = await self.provider.eth.subscribe('newPendingTransactions')

        try:
            while True:
                transaction_hash = await subscription.get_new_transaction()
                await self.handle_transaction(transaction_hash)
        except Exception as e:
            print(f"Error in observer loop: {e}")
