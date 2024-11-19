from datetime import datetime, timedelta, timezone
from http import HTTPStatus as status

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from loguru import logger
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.database import pool
from app.config import API_CONFIG_HASHING_ALGORITHM, API_CONFIG_SERVER_SECRET_KEY


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/accounts/login")


# Function to check if user with the given email already exists
async def get_user(email: str) -> dict:
    async with pool.acquire() as connection:
        stmt = f"SELECT * FROM Employees WHERE Email = ?"
        stmt_exec = await connection.execute(stmt, (email,))
        result = await stmt_exec.fetchone()
        logger.info(f"Checking if user with email {email} exists")
        await connection.close()
        return result


async def get_employee_code_in_device(employee_code: str) -> str:
    async with pool.acquire() as connection:
        stmt = f"SELECT EmployeeCodeInDevice FROM Employees WHERE EmployeeCode = ?"
        stmt_exec = await connection.execute(stmt, (employee_code,))
        result = await stmt_exec.fetchone()
        logger.info(f"Checking if user with employee code {employee_code} exists")
        await connection.close()
        return result[0] if result else None


# Function to verify password
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="Unknown hash algorithm used",
        )


# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=API_CONFIG_SERVER_SECRET_KEY,
        algorithm=API_CONFIG_HASHING_ALGORITHM,
    )
    return encoded_jwt


# Function to get current user from token
def get_user_email(token: str = Depends(oauth2scheme)):
    try:
        payload = jwt.decode(
            token,
            key=API_CONFIG_SERVER_SECRET_KEY,
            algorithms=[API_CONFIG_HASHING_ALGORITHM],
        )

        if not (email := payload.get("sub")):
            raise HTTPException(status_code=status.FORBIDDEN, detail="Invalid token")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.FORBIDDEN, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.FORBIDDEN, detail="Invalid token")

    return email
