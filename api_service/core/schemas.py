from pydantic import BaseModel

# Defined base schemas for inheritance


class StatusOkSchema(BaseModel):
    status: str = "ok"


class CountSchema(BaseModel):
    count: int
