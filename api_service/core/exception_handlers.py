from main import app
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {"non_field_error": []}
    for error in exc.errors():
        field_path = ".".join(
            str(x) for x in error["loc"] if not isinstance(x, int) and x != "body"
        )
        error_key = (
            "error.validation."
            + error["type"]
            + ("." + field_path if field_path else "")
        )
        if not field_path or any(isinstance(x, int) for x in error["loc"]):
            errors["non_field_error"].append(error_key)
        else:
            errors[field_path] = error_key
    return JSONResponse(status_code=400, content={"errors": errors, "status": "error"})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.detail, "status": "error"}
    )


@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 500:
        return JSONResponse(
            status_code=500,
            content={"error": "error.server.internal_error", "status": "error"},
        )

    return await http_exception_handler(request, exc)
