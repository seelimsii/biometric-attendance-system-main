from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from app.accounts.router import router as accounts_router
from app.database import metadata, engine, pool
from app.geofencing.router import router as geofencing_router
from app.mics.router import router as mics_router
from app.attendance.router import router as attendance_router
from app.leaves.router import router as leaves_router
from app.utils import db_table_creation


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server starting...")
    await db_table_creation(metadata=metadata, engine=engine)

    yield
    pool.close()
    await pool.wait_closed()
    logger.info("Closed DB connection")
    logger.info("Server exiting...")


# Create an instance of FastAPI
app = FastAPI(lifespan=lifespan)

# Include the routers
app.include_router(accounts_router, prefix="/api/v1/accounts", tags=["Accounts"])
app.include_router(geofencing_router, prefix="/api/v1/geofencing", tags=["Geofencing"])
app.include_router(mics_router, prefix="/api/v1/mics", tags=["Mics"])
app.include_router(attendance_router, prefix="/api/v1/attendance", tags=["Attendance"])
app.include_router(leaves_router, prefix="/api/v1/leaves", tags=["Leaves"])


# Define exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"detail": detail},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors(include_url=False)}")
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"detail": detail},
    )


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors(include_url=False)}")
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"detail": detail},
    )


# Define a route using a decorator
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
