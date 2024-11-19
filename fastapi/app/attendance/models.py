from typing import Optional, List

from pydantic import BaseModel
from datetime import date, timedelta, datetime


# Base template with common fields
class AttendanceViewBaseModel(BaseModel):
    Duration: Optional[timedelta] = None


# AttendanceView extending the base template
class AttendanceView(AttendanceViewBaseModel):
    AttendanceDate: Optional[date] = None
    InTime: Optional[datetime] = None
    OutTime: Optional[datetime] = None
    WeeklyOff: Optional[bool] = None


# WeeklyAttendanceView extending the base template
class WeeklyAttendanceView(AttendanceViewBaseModel):
    Attendance: List[AttendanceView] = []
    AverageInTime: Optional[str] = None
    AverageOutTime: Optional[str] = None
    Present: Optional[int] = None
    Absent: Optional[int] = None


# MonthlyAttendanceView extending the base template
class MonthlyAttendanceView(AttendanceViewBaseModel):
    Attendance: List[AttendanceView] = []
    AverageInTime: Optional[str] = None
    AverageOutTime: Optional[str] = None
    Present: Optional[int] = None
    Absent: Optional[int] = None
    Leave: Optional[int] = None
