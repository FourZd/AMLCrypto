from fastapi import FastAPI
from core.container import Container
from transactions.router import router as transactions_router

app = FastAPI()

container = Container()
container.init_resources()
container.wire(modules=[__name__])

app.include_router(transactions_router)