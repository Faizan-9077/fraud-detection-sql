from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routes.health import router as health_router
from api.routes.query import router as query_router

from api.exceptions import (
    QueryGenerationError,
    DatabaseExecutionError,
)

from query_engine.services.sql_validator import SQLValidationError


app = FastAPI(
    title="AML Fraud Detection API",
    description="Natural Language to SQL API for AML Fraud Detection",
    version="1.0.0",
)


@app.exception_handler(SQLValidationError)
async def sql_validation_exception_handler(
    request: Request,
    exc: SQLValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": str(exc),
        },
    )


@app.exception_handler(QueryGenerationError)
async def query_generation_exception_handler(
    request: Request,
    exc: QueryGenerationError,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
        },
    )


@app.exception_handler(DatabaseExecutionError)
async def database_exception_handler(
    request: Request,
    exc: DatabaseExecutionError,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Unexpected server error.",
        },
    )


app.include_router(
    health_router,
    tags=["Health"]
)

app.include_router(
    query_router,
    tags=["AML Query"]
)