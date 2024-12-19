from fastapi import FastAPI
from core.container import Container


app = FastAPI()

container = Container()
container.init_resources()
container.wire(modules=[__name__])