from fastapi import APIRouter, Depends, Query, HTTPException
from dependency_injector.wiring import Provide, inject
from core.container import Container
from .schemas import GetTransactionsResponse, GetTransactionStatsResponse, GetTransactionResponse
from .services import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.get("/stats/", response_model=GetTransactionStatsResponse)
@inject
async def get_transaction_stats(
    tx_service: TransactionService = Depends(Provide[Container.transaction_service])
):
    stats = await tx_service.get_transaction_stats()
    return GetTransactionStatsResponse(data=stats)


@router.get("/{transaction_hash:str}/", response_model=GetTransactionResponse)
@inject
async def get_transaction(
    transaction_hash: str, tx_service: TransactionService = Depends(Provide[Container.transaction_service])
):
    try:
        transaction = await tx_service.get_transaction(transaction_hash)
        return GetTransactionResponse(data=transaction)
    except ValueError:
        raise HTTPException(status_code=404, detail="Transaction not found")


@router.get("/", response_model=GetTransactionsResponse)
@inject
async def get_transactions(
    block_id: int = Query(None, ge=1),
    sender: str = Query(None),
    recipient: str = Query(None),

    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    tx_service: TransactionService = Depends(Provide[Container.transaction_service])
):
    transactions, count = await tx_service.get_transactions(
        block_id, sender, recipient, limit, offset
    )
    return GetTransactionsResponse(data=transactions, count=count)


