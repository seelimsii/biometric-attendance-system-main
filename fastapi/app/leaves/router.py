from datetime import datetime
from http import HTTPStatus as status

from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from app.accounts.utils import get_user, get_user_email
from app.database import pool, CommonResponse
from app.leaves.common import LeaveTypeRequestModel, LeaveEntryRequestModel
from app.leaves.models import LeaveEntry
from app.leaves.queries import (
    create_leave_type_stmt,
    get_leaves_type_stmt,
    update_leave_type_stmt,
    create_leave_stmt,
)
from app.utils import rdict

router = APIRouter()


@router.post("/create-leave-type")
async def create_leave_type(leave_type: LeaveTypeRequestModel):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Execute the insertion query
                await cursor.execute(
                    create_leave_type_stmt, *leave_type.model_dump().values()
                )
                await conn.commit()

                # Fetch the last inserted id using IDENT_CURRENT
                await cursor.execute("SELECT IDENT_CURRENT('LeaveTypes')")
                leave_type_id = (await cursor.fetchone())[0]

                # Fetch the inserted record
                await cursor.execute(
                    "SELECT * FROM LeaveTypes WHERE LeaveTypeID = ?",
                    leave_type_id,
                )
                leave_type = await cursor.fetchone()
                return CommonResponse(
                    status="success",
                    message="Leave type created successfully",
                    data={"LeaveType": rdict(leave_type)},
                )
    except Exception as e:
        logger.error(f"Error occurred while creating leave type: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating leave type",
        )


@router.get("/get-leave-types/{leave_type_id}")
async def get_leave_types(leave_type_id: int = None):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if leave_type_id and leave_type_id > 0:
                    await cursor.execute(
                        "SELECT * FROM LeaveTypes WHERE LeaveTypeID = ?",
                        leave_type_id,
                    )
                    leave_type = await cursor.fetchone()
                    return CommonResponse(
                        status="success",
                        message="Leave type retrieved successfully",
                        data={"LeaveType": rdict(leave_type)},
                    )

                await cursor.execute(get_leaves_type_stmt)
                leave_types = await cursor.fetchall()
                return CommonResponse(
                    status="success",
                    message="Leave types retrieved successfully",
                    data={
                        "LeaveTypes": [rdict(leave_type) for leave_type in leave_types]
                    },
                )
    except Exception as e:
        logger.error(f"Error occurred while fetching leave types: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching leave types",
        )


@router.patch("/update-leave-type/{leave_type_id}")
async def update_leave_type(leave_type_id: int, leave_type: LeaveTypeRequestModel):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    update_leave_type_stmt,
                    leave_type.LeaveTypeFName,
                    leave_type.LeaveTypeSName,
                    leave_type.CarryForwardLimit,
                    leave_type.Gender,
                    leave_type.YearlyLimit,
                    leave_type.ConsiderWeeklyOff,
                    leave_type.ConsiderHoliday,
                    leave_type.MarkedAs,
                    leave_type.Description,
                    leave_type.RecordStatus,
                    leave_type.IsAllowNegativeBalance,
                    leave_type_id,
                )
                await conn.commit()
                await cursor.execute(
                    "SELECT * FROM LeaveTypes WHERE LeaveTypeID = ?",
                    leave_type_id,
                )
                leave_type = await cursor.fetchone()
                return CommonResponse(
                    status="success",
                    message="Leave type updated successfully",
                    data={"LeaveType": rdict(leave_type)},
                )
    except Exception as e:
        logger.error(f"Error occurred while updating leave type: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating leave type",
        )


@router.delete("/delete-leave-type/{leave_type_id}")
async def delete_leave_type(leave_type_id: int):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM LeaveTypes WHERE LeaveTypeID = ?", leave_type_id
                )
                await conn.commit()
                return CommonResponse(
                    status="success",
                    message="Leave type deleted successfully",
                )
    except Exception as e:
        logger.error(f"Error occurred while deleting leave type: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting leave type",
        )


@router.post("/create-leave")
async def create_leave(
    request: LeaveEntryRequestModel,
    email: str = Depends(get_user_email),
):
    if not (user := await get_user(email)):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="Unauthorized user",
        )

    leave = LeaveEntry(
        LeaveTypeId=request.LeaveTypeId,
        EmployeeId=user.EmployeeCode,
        FromDate=request.FromDate,
        ToDate=request.ToDate,
        Remarks=request.Remarks,
        LastModifiedBy=user.EmployeeCode,
        CreatedDate=datetime.now(),
        LastModifiedDate=datetime.now(),
    )

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    create_leave_stmt,
                    *leave.model_dump().values(),
                )
                leave = await cursor.fetchone()
                await conn.commit()
                return CommonResponse(
                    status="success",
                    message="Leave created successfully",
                    data={"leave": rdict(leave)},
                )
    except Exception as e:
        logger.error(f"Error occurred while creating leave: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating leave",
        )


@router.get("/get-leaves/{leave_id}")
async def get_leaves(leave_id: int = None):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if leave_id and leave_id > 0:
                    await cursor.execute(
                        "SELECT * FROM LeaveEntries WHERE LeaveEntryId = ?",
                        leave_id,
                    )
                    leave = await cursor.fetchone()
                    return CommonResponse(
                        status="success",
                        message="Leave retrieved successfully",
                        data={"Leave": rdict(leave)},
                    )

                await cursor.execute("SELECT * FROM LeaveEntries")
                leaves = await cursor.fetchall()
                return CommonResponse(
                    status="success",
                    message="Leaves retrieved successfully",
                    data={"Leaves": [rdict(leave) for leave in leaves]},
                )
    except Exception as e:
        logger.error(f"Error occurred while fetching leaves: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching leaves",
        )


@router.patch("/update-leave/{leave_id}")
async def update_leave(
    leave_id: int,
    leave: LeaveEntryRequestModel,
    email: str = Depends(get_user_email),
):
    if not (user := await get_user(email)):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="Unauthorized user",
        )

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """UPDATE LeaveEntries SET
                        LeaveTypeId = ?,
                        FromDate = ?,
                        ToDate = ?,
                        Remarks = ?,
                        LastModifiedBy = ?,
                        LastModifiedDate = ?
                    WHERE LeaveEntryId = ?""",
                    leave.LeaveTypeId,
                    leave.FromDate,
                    leave.ToDate,
                    leave.Remarks,
                    user.EmployeeCode,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    leave_id,
                )
                await conn.commit()
                await cursor.execute(
                    "SELECT * FROM LeaveEntries WHERE LeaveEntryId = ?",
                    leave_id,
                )
                if not (leave := await cursor.fetchone()):
                    raise HTTPException(
                        status_code=status.NOT_FOUND,
                        detail="Leave not found",
                    )

                return CommonResponse(
                    status="success",
                    message="Leave updated successfully",
                    data={"Leave": rdict(leave)},
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while updating leave: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating leave",
        )


@router.delete("/delete-leave/{leave_id}")
async def delete_leave(leave_id: int, email: str = Depends(get_user_email)):
    if not (user := await get_user(email)):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="Unauthorized user",
        )

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """DELETE FROM LeaveEntries
                    WHERE LeaveEntryId = ? AND EmployeeId = ?""",
                    leave_id,
                    user.EmployeeCode,
                )
                await conn.commit()
                return CommonResponse(
                    status="success",
                    message="Leave deleted successfully",
                    data={"LeaveId": leave_id},
                )
    except Exception as e:
        logger.error(f"Error occurred while deleting leave: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting leave",
        )


@router.patch("/approve-leave/{leave_id}")
async def approve_leave(leave_id: int, email: str = Depends(get_user_email)):
    if not (user := await get_user(email)):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="Unauthorized user",
        )

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """UPDATE LeaveEntries SET
                        IsApproved = 1,
                        ApprovedBy = ?
                    WHERE LeaveEntryId = ?""",
                    user.EmployeeCode,
                    leave_id,
                )
                await conn.commit()
                await cursor.execute(
                    "SELECT * FROM LeaveEntries WHERE LeaveEntryId = ?",
                    leave_id,
                )
                if not (leave := await cursor.fetchone()):
                    raise HTTPException(
                        status_code=status.NOT_FOUND,
                        detail="Leave not found",
                    )

                return CommonResponse(
                    status="success",
                    message="Leave approved successfully",
                    data={"Leave": rdict(leave)},
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while approving leave: {e=}")
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail="An error occurred while approving leave",
        )
