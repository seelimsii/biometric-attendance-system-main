from datetime import datetime, timedelta
from http import HTTPStatus as status

from fastapi import HTTPException
from loguru import logger

from app.database import pool
from app.attendance.models import AttendanceView


async def get_attendance_of_day(
    emp_code_in_device: int,
    current_datetime: datetime,
    midnight_datetime: datetime,
    db_name: str,
):
    logger.info(f"Fetching attendance < {current_datetime} > {midnight_datetime}")
    stmt = f"""
            SELECT LogDate FROM {db_name}
            WHERE UserId = ? 
            AND LogDate < ? 
            AND LogDate > ? 
            ORDER BY LogDate ASC;"""

    async with pool.acquire() as connection:
        try:
            stmt_exec = await connection.execute(
                stmt,
                (
                    emp_code_in_device,
                    current_datetime,
                    midnight_datetime,
                ),
            )
            result = await stmt_exec.fetchall()
        except Exception as e:
            logger.error(f"Error fetching attendance: {e}")
            raise HTTPException(
                status_code=status.INTERNAL_SERVER_ERROR,
                detail="Error fetching attendance",
            )
        finally:
            await connection.close()

    if not result:
        return None

    checks = [x[0] for x in result if x]
    logger.info(f"Attendance found for {current_datetime}: {result}")

    duration = timedelta()
    for i in range(0, len(checks), 2):
        if i + 1 < len(checks):
            duration += checks[i + 1] - checks[i]

    return AttendanceView(
        AttendanceDate=current_datetime.date(),
        InTime=checks[0] if checks else None,
        OutTime=checks[-2] if len(checks) % 2 else checks[-1],
        Duration=duration,
        WeeklyOff=True if current_datetime.today().weekday() in [5, 6] else False,
    )


def calculate_average_in_time(attendance: list):
    return sum(
        [attendance.InTime.hour for attendance in attendance if attendance.InTime]
    ) // len(attendance)


def calculate_average_out_time(attendance: list):
    return sum(
        [attendance.OutTime.hour for attendance in attendance if attendance.OutTime]
    ) // len(attendance)


def calculate_duration(attendance: list):
    duration = timedelta()
    for attendance in attendance:
        if attendance.Duration:
            duration += attendance.Duration

    return duration


def calculate_present_days(attendance: list):
    return len([attendance for attendance in attendance if attendance.Duration])


def calculate_absent_days(attendance: list):
    return len([attendance for attendance in attendance if not attendance.Duration])
