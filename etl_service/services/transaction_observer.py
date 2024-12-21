from web3 import AsyncWeb3
from web3.providers.persistent import WebSocketProvider
from services.message_broker import MessageBroker
from datetime import datetime
from core.logger import logger
from schemas.transaction_schemas import Transaction


class TransactionObserver:
    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker

    async def observe(self, provider_url: str, queue_name: str):
        """Async method to observe new blocks and publish transactions to the message broker"""
        async with AsyncWeb3(WebSocketProvider(provider_url)) as w3:
            logger.info("Subscribing to new heads")
            subscription = await w3.eth.subscribe('newHeads')
            logger.info(f"Subscription confirmed {subscription}")
            async for response in w3.socket.process_subscriptions():
                logger.info(f"Response received! {response}")
                block_hash = response.get('result', {}).get('hash')
                if block_hash:
                    logger.info(f"Handling new block {block_hash}")
                    formatted_transactions = await self.handle_new_block(w3, block_hash)
                    await self.message_broker.publish_to_queue(formatted_transactions, queue_name)
                else:
                    logger.warning("Block hash is missing in the response")

    async def handle_new_block(self, w3: AsyncWeb3, block_hash: str):
        """Handles a new block, gets transactions and formats them"""
        try:
            logger.info(f"Getting info about the block {block_hash}")
            block = await w3.eth.get_block(block_hash, full_transactions=True)
            logger.info(f"Block data: {block}")
            transactions = []
            for tx in block.transactions:
                logger.info(f"Processing tx {tx.hash.hex()}")
                transaction_details = self.format_transaction(block, tx)
                logger.info(f"Tx details: {transaction_details}")
                transactions.append(transaction_details)
            return transactions
        except Exception as e:
            logger.error(f"Error processing block {block_hash}: {e}")

    def format_transaction(self, block, transaction):
        """Formats a transaction to a Transaction DTO"""
        try:
            return Transaction(
                block_id=block.number,
                index=str(transaction.transactionIndex),
                hash=transaction.hash.hex(),
                time=datetime.utcfromtimestamp(block.timestamp).isoformat(),
                sender=transaction["from"],
                recipient=transaction.to or "",
                value=str(transaction.value),
                fee=transaction.gas * transaction.gasPrice if transaction.gasPrice else None,
                gas_limit=transaction.gas,
                input_hex=str(transaction.input),
                nonce=transaction.nonce,
            )
        except Exception as e:
            logger.error(f"Error formatting transaction {transaction.hash.hex()}: {e}")
            return None
