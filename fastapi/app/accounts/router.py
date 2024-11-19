from datetime import timedelta
from http import HTTPStatus as status

from pyodbc import IntegrityError
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from app.accounts.common import ForgetPasswordRequestModel, UserRegistrationRequestModel
from app.accounts.utils import (
    pwd_context,
    verify_password,
    create_access_token,
    get_user,
    get_user_email,
)
from app.config import API_CONFIG_ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import pool


router = APIRouter()


@router.post("/bulk-user-upload")
async def upload_bulk_users(file: UploadFile = File(...)):
    """
    Bulk upload users from a CSV file
    """

    async def read_lines(file: UploadFile):
        while True:
            line = await file.read(1024)  # Read in chunks
            if not line:
                break
            yield line.decode("utf-8")

    async def process_file(file: UploadFile):
        users = []
        buffer = ""
        try:
            async for chunk in read_lines(file):
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line:
                        continue

                    user = line.strip().split(",")
                    if user[0] == "EmployeeName":
                        continue

                    users.append(tuple(user))
            return users
        except Exception as e:
            logger.error(f"Error occurred while processing file: {e=}")
            raise HTTPException(
                status_code=status.BAD_REQUEST,
                detail="Error occurred while processing file",
            )

    async def insert_users(users):
        logger.debug(users)
        async with pool.acquire() as connection:
            insert_query = """
            INSERT INTO Employees (
                EmployeeName, EmployeeCode, StringCode, NumericCode,
                Gender, CompanyId, DepartmentId, CategoryId,
                EmployeeCodeInDevice, EmployementType, Status, Email
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                cursor = await connection.cursor()
                await cursor.executemany(insert_query, users)
                await connection.commit()
            finally:
                await cursor.close()
                await connection.close()

    try:
        users = await process_file(file)
        await insert_users(users)
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        logger.error(f"Error occurred while bulk uploading users: {e=}")
        raise HTTPException(
            status_code=status.BAD_REQUEST,
            detail="User with this EmployeeCode already exists",
        )
    except Exception as e:
        logger.error(f"Error occurred while bulk uploading users: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="Error occurred while bulk uploading users",
        )

    return {"message": "Users uploaded successfully"}


@router.patch("/register")
async def register_user(request: UserRegistrationRequestModel):
    if not (user := await get_user(request.email)):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="User with this email is not permitted to register",
        )

    if user.LoginPassword:
        raise HTTPException(
            status_code=status.BAD_REQUEST,
            detail="User with this email already exists",
        )

    hashed_password = pwd_context.hash(request.password)
    try:
        async with pool.acquire() as connection:
            try:
                await connection.execute(
                    "UPDATE Employees SET LoginPassword = ? WHERE Email = ?",
                    (hashed_password, request.email),
                )
                await connection.commit()
                return JSONResponse(
                    status_code=status.CREATED,
                    content={"message": "Registration successful"},
                )
            except Exception as e:
                logger.error(f"Error occurred while updating password: {e}")
                raise HTTPException(
                    status_code=status.INTERNAL_SERVER_ERROR,
                    detail="Error occurred while updating password",
                )
            finally:
                await connection.close()

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while registering user: {e}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="Error occurred while registering user",
        )


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    try:
        async with pool.acquire() as connection:
            stmt = f"SELECT * FROM Employees WHERE Email = ?"
            result = await connection.execute(stmt, (request.username,))
            db_user = await result.fetchone()
            if not db_user:
                raise HTTPException(
                    status_code=status.UNAUTHORIZED,
                    detail="Incorrect email or password",
                )

            # Check if user exists and password is correct
            if verify_password(request.password, db_user.LoginPassword):
                access_token_expires = timedelta(
                    minutes=API_CONFIG_ACCESS_TOKEN_EXPIRE_MINUTES
                )
                access_token = create_access_token(
                    data={"sub": db_user.Email},
                    expires_delta=access_token_expires,
                )
                await connection.close()
                return {"access_token": access_token, "token_type": "bearer"}

            raise HTTPException(
                status_code=status.UNAUTHORIZED,
                detail="Incorrect email or password",
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while logging in: {e}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="Error occurred while logging in",
        )
    finally:
        await connection.close()


@router.patch("/change-password")
async def change_password(request: ForgetPasswordRequestModel):
    if request.old_password == request.new_password:
        raise HTTPException(
            status_code=status.BAD_REQUEST,
            detail="Old password and new password cannot be the same",
        )

    if not (db_user := await get_user(request.email)):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="User with this email is not permitted to change password",
        )

    if not verify_password(request.old_password, db_user.LoginPassword):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    hashed_password = pwd_context.hash(request.new_password)
    try:
        async with pool.acquire() as connection:
            await connection.execute(
                "UPDATE Employees SET LoginPassword = ? WHERE Email = ?",
                (hashed_password, request.email),
            )
            await connection.commit()
    except Exception as e:
        logger.error(f"Error occurred while changing password: {e}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="Error occurred while changing password",
        )
    finally:
        await connection.close()


@router.get("/me")
async def get_current_user(email: str = Depends(get_user_email)):
    try:
        if not (user := await get_user(email)):
            raise HTTPException(
                status_code=status.UNAUTHORIZED,
                detail="User with this email is not permitted to access this resource",
            )

        return {
            "EmployeeName": user.EmployeeName,
            "EmployeeCode": user.EmployeeCode,
            "StringCode": user.StringCode,
            "NumericCode": user.NumericCode,
            "Gender": user.Gender,
            "CompanyId": user.CompanyId,
            "DepartmentId": user.DepartmentId,
            "CategoryId": user.CategoryId,
            "EmployementType": user.EmployementType,
            "Status": user.Status,
            "Email": user.Email,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while getting current user: {e}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="Error occurred while getting current user",
        )
