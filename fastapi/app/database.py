import asyncio
from typing import Optional

import aioodbc
import nest_asyncio
from pydantic import BaseModel
from sqlalchemy import URL
from sqlalchemy import create_engine, MetaData

from app.config import (
    API_CONFIG_MSSQL_USERNAME as username,
    API_CONFIG_MSSQL_PASSWORD as password,
    API_CONFIG_MSSQL_SERVER_NAME as server_name,
    API_CONFIG_MSSQL_DB_NAME as db_name,
    API_CONFIG_DB_CONNECTION_POOL_SIZE as pool_size,
)


dsn = (
    "Driver={ODBC Driver 17 for SQL Server};Server="
    + server_name
    + ";Database="
    + db_name
    + ";UID="
    + username
    + f";PWD="
    + password
)

metadata = MetaData()
engine = create_engine(
    url=URL.create(
        drivername="mssql+pyodbc",
        username=username,
        password=password,
        host=server_name,
        database=db_name,
        query={"driver": "ODBC Driver 17 for SQL Server"},
    )
)

nest_asyncio.apply()

loop = asyncio.get_event_loop()
pool = loop.run_until_complete(aioodbc.create_pool(dsn=dsn, maxsize=pool_size))


class CommonResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict]
