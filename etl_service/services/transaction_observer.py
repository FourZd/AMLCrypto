from web3 import AsyncWeb3
from web3.providers.persistent import WebSocketProvider
from services.message_broker import MessageBroker
from datetime import datetime


class TransactionObserver:
    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker

    async def observe(self, provider_url: str):
        """Асинхронный метод для наблюдения за завершёнными транзакциями"""
        async with AsyncWeb3(WebSocketProvider(provider_url)) as w3:
            subscription = await w3.eth.subscribe('newHeads')  # Подписка на новые блоки
            async for response in w3.socket.process_subscriptions():
                block_hash = response.get('hash')
                if block_hash:
                    await self.handle_new_block(w3, block_hash)

    async def handle_new_block(self, w3: AsyncWeb3, block_hash: str):
        """Обработка нового блока"""
        try:
            block = await w3.eth.get_block(block_hash, full_transactions=True)  # С полными транзакциями
            transactions = block.transactions

            for tx in transactions:
                transaction_details = self.format_transaction(w3, block, tx)
                if transaction_details:
                    await self.message_broker.send(transaction_details)

        except Exception as e:
            print(f"Error processing block {block_hash}: {e}")

    def format_transaction(self, w3: AsyncWeb3, block, transaction):
        """Форматирует данные транзакции в нужный формат"""
        try:
            receipt = w3.eth.get_transaction_receipt(transaction.hash)
            return {
                "block_id": block.number,
                "index": transaction.transactionIndex,
                "hash": transaction.hash.hex(),
                "time": datetime.utcfromtimestamp(block.timestamp).isoformat(),
                "failed": int(receipt.status == 0),
                "type": transaction.type,
                "sender": transaction["from"],
                "recipient": transaction.to or "",
                "call_count": len(receipt.logs),
                "value": str(transaction.value),
                "value_usd": self.estimate_value_in_usd(transaction.value),
                "internal_value": "0",
                "internal_value_usd": 0.0,
                "fee": int(receipt.gasUsed * transaction.gasPrice),
                "fee_usd": self.estimate_value_in_usd(receipt.gasUsed * transaction.gasPrice),
                "gas_used": receipt.gasUsed,
                "gas_limit": transaction.gas,
                "gas_price": transaction.gasPrice,
                "input_hex": transaction.input,
                "nonce": transaction.nonce,
                "v": transaction.v,
                "r": int(transaction.r, 16),
                "s": int(transaction.s, 16),
            }
        except Exception as e:
            print(f"Error formatting transaction {transaction.hash.hex()}: {e}")
            return None

    def estimate_value_in_usd(self, value: int):
        """Пример оценки стоимости в USD. Требует подключения к стороннему API."""
        eth_to_usd = 2000  # Заглушка для курса ETH
        return float(value) / 10**18 * eth_to_usd
