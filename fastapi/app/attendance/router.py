from datetime import datetime, timedelta
from http import HTTPStatus as status

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.utils import rdict
from app.accounts.utils import get_user_email, get_user, get_employee_code_in_device
from app.attendance.models import AttendanceView, WeeklyAttendanceView
from app.attendance.utils import (
    get_attendance_of_day,
    calculate_average_in_time,
    calculate_average_out_time,
    calculate_present_days,
    calculate_absent_days,
    calculate_duration,
)

router = APIRouter()


@router.get(path="/today", status_code=status.OK)
async def get_attendance(email: str = Depends(get_user_email)):
    user = rdict(await get_user(email))
    user_employee_code = user.get("EmployeeCode")
    user_emp_code_in_device = await get_employee_code_in_device(user_employee_code)
    if not user_emp_code_in_device:
        raise HTTPException(
            status_code=status.NOT_FOUND,
            detail="Employee code not found in the device",
        )

    current_datetime = datetime.now()
    midnight = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    attendance = await get_attendance_of_day(
        emp_code_in_device=user_emp_code_in_device,
        current_datetime=current_datetime,
        midnight_datetime=midnight,
        db_name=f"DeviceLogs_{current_datetime.month}_{current_datetime.year}",
    )

    if not attendance:
        return AttendanceView()

    return AttendanceView(
        AttendanceDate=attendance.AttendanceDate,
        InTime=attendance.InTime,
        OutTime=attendance.OutTime,
        Duration=attendance.Duration,
        WeeklyOff=attendance.WeeklyOff,
    )


@router.get(path="/weekly/{offset}", status_code=status.OK)
async def get_weekly_attendance(email: str = Depends(get_user_email), offset: int = 0):
    user = rdict(await get_user(email))
    user_employee_code = user.get("EmployeeCode")
    user_emp_code_in_device = await get_employee_code_in_device(user_employee_code)
    if not user_emp_code_in_device:
        raise HTTPException(
            status_code=status.NOT_FOUND,
            detail="Employee code not found in the device",
        )

    # get start day of week using offset
    current_datetime = datetime.now()
    midnight = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    start_of_week = (
        midnight
        + timedelta(days=-current_datetime.weekday())
        + timedelta(days=offset * 7)
    )
    logger.info(f"Start of week: {start_of_week}")

    weekly_attendance = []
    for i in range(min(7, current_datetime.weekday() + 1)):
        start_of_week += timedelta(days=i)
        attendance = await get_attendance_of_day(
            emp_code_in_device=user_emp_code_in_device,
            current_datetime=start_of_week
            + timedelta(hours=23, minutes=59, seconds=59),
            midnight_datetime=start_of_week,
            db_name=f"DeviceLogs_{current_datetime.month}_{current_datetime.year}",
        )

        if not attendance:
            continue

        weekly_attendance.append(
            AttendanceView(
                AttendanceDate=attendance.AttendanceDate,
                InTime=attendance.InTime,
                OutTime=attendance.OutTime,
                Duration=attendance.Duration,
                WeeklyOff=attendance.WeeklyOff,
            )
        )

    if not weekly_attendance:
        return WeeklyAttendanceView(
            Duration=timedelta(),
            Attendance=[],
            AverageInTime="00:00",
            AverageOutTime="00:00",
            Present=0,
            Absent=7,
        )

    duration = timedelta()
    for attendance in weekly_attendance:
        if attendance.Duration:
            duration += attendance.Duration

    AverageInTime = sum(
        [
            attendance.InTime.hour
            for attendance in weekly_attendance
            if attendance.InTime
        ]
    ) // len(weekly_attendance)

    AverageOutTime = sum(
        [
            attendance.OutTime.hour
            for attendance in weekly_attendance
            if attendance.OutTime
        ]
    ) // len(weekly_attendance)

    Present = len(
        [attendance for attendance in weekly_attendance if attendance.Duration]
    )

    Absent = len(
        [attendance for attendance in weekly_attendance if not attendance.Duration]
    )

    return WeeklyAttendanceView(
        EmployeeCode=user_employee_code,
        EmployeeName=user.get("EmployeeName"),
        Duration=duration,
        Attendance=weekly_attendance,
        AverageInTime=f"{AverageInTime}:00",
        AverageOutTime=f"{AverageOutTime}:00",
        Present=Present,
        Absent=Absent,
    )


@router.get(path="/monthly/{offset}", status_code=status.OK)
async def get_monthly_attendance(email: str = Depends(get_user_email), offset: int = 0):
    user_info = rdict(await get_user(email))
    employee_code = user_info.get("EmployeeCode")
    device_employee_code = await get_employee_code_in_device(employee_code)

    if not device_employee_code:
        raise HTTPException(
            status_code=status.NOT_FOUND,
            detail="Employee code not found in the device",
        )

    current_datetime = datetime.now()
    start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    start_of_month = start_of_day.replace(day=1)
    start_of_month = start_of_month.replace(month=start_of_month.month + offset)
    logger.info(f"Start of month: {start_of_month}")

    total_days_in_month = (
        start_of_month.replace(month=start_of_month.month + 1) - start_of_month
    ).days

    days_to_check = (
        min(total_days_in_month, current_datetime.day + 1)
        if offset == 0
        else total_days_in_month
    )

    current_date = start_of_month

    monthly_attendance_records = []
    for _ in range(0, days_to_check + 1):
        if current_date.month != start_of_month.month:
            break

        end_of_day = current_date + timedelta(hours=23, minutes=59, seconds=59)
        attendance_record = await get_attendance_of_day(
            emp_code_in_device=device_employee_code,
            current_datetime=end_of_day,
            midnight_datetime=current_date,
            db_name=f"DeviceLogs_{start_of_month.month}_{start_of_month.year}",
        )

        if not attendance_record:
            current_date += timedelta(days=1)
            continue

        monthly_attendance_records.append(
            AttendanceView(
                AttendanceDate=attendance_record.AttendanceDate,
                InTime=attendance_record.InTime,
                OutTime=attendance_record.OutTime,
                Duration=attendance_record.Duration,
                WeeklyOff=attendance_record.WeeklyOff,
            )
        )

        current_date += timedelta(days=1)

    if not monthly_attendance_records:
        return WeeklyAttendanceView(
            Duration=timedelta(),
            Attendance=[],
            AverageInTime="00:00",
            AverageOutTime="00:00",
            Present=0,
            Absent=30,
        )

    absent_days = calculate_absent_days(monthly_attendance_records)
    average_in_time = calculate_average_in_time(monthly_attendance_records)
    average_out_time = calculate_average_out_time(monthly_attendance_records)
    total_duration = calculate_duration(monthly_attendance_records)
    present_days = calculate_present_days(monthly_attendance_records)

    return WeeklyAttendanceView(
        EmployeeCode=employee_code,
        EmployeeName=user_info.get("EmployeeName"),
        Duration=total_duration,
        Attendance=monthly_attendance_records,
        AverageInTime=f"{average_in_time}:00",
        AverageOutTime=f"{average_out_time}:00",
        Present=present_days,
        Absent=absent_days,
    )
