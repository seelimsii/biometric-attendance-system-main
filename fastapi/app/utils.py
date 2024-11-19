import asyncio

from loguru import logger
from pyodbc import Row
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import MetaData
from sqlalchemy.engine.base import Engine

from app.config import (
    API_CONFIG_DB_CONNECTION_RETRY_INTERVAL,
    API_CONFIG_MAX_DB_CONNECTION_RETRIES,
)


async def db_table_creation(metadata: MetaData, engine: Engine):
    retries = 0
    while retries < API_CONFIG_MAX_DB_CONNECTION_RETRIES:
        try:
            metadata.create_all(engine)
            logger.info("Initialized all tables in MSSQL")
            return  # Success, exit loop
        except ProgrammingError as pe:
            logger.error(f"Failed to create tables: {pe}")
            retries += 1
            await asyncio.sleep(API_CONFIG_DB_CONNECTION_RETRY_INTERVAL)

    logger.error("Failed to initialize tables in MSSQL after retries.")
    raise SystemExit(1)


def rdict(row: Row) -> dict:
    """
    Convert a pyodbc.Row object to a dictionary
    """
    return dict(zip([t[0] for t in row.cursor_description], row))
