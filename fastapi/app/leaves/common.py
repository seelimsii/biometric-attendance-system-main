from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class LeaveTypeRequestModel(BaseModel):
    LeaveTypeFName: str = Field(
        ...,
        max_length=50,
        title="Leave Type Full Name",
        description="Full name of the leave type",
    )
    LeaveTypeSName: str = Field(
        ...,
        max_length=50,
        title="Leave Type Short Name",
        description="Short name of the leave type",
    )
    CarryForwardLimit: int = Field(
        0,
        title="Carry Forward Limit",
        description="Maximum number of unused leave days that can be carried forward to the next year",
    )
    Gender: str = Field(
        ...,
        max_length=255,
        title="Gender",
        description="Gender specific leave, if applicable",
    )
    YearlyLimit: str = Field(
        "0",
        max_length=50,
        title="Yearly Limit",
        description="Maximum number of leave days that can be taken in a year",
    )
    ConsiderWeeklyOff: int = Field(
        ...,
        title="Consider Weekly Off",
        description="Indicates whether weekly off days are considered in the leave count",
    )
    ConsiderHoliday: int = Field(
        ...,
        title="Consider Holiday",
        description="Indicates whether holidays are considered in the leave count",
    )
    MarkedAs: Optional[str] = Field(
        None,
        max_length=255,
        title="Marked As",
        description="Status or categorization for the leave type",
    )
    Description: Optional[str] = Field(
        None,
        max_length=255,
        title="Description",
        description="Description of the leave type",
    )
    RecordStatus: Optional[int] = Field(
        1,
        title="Record Status",
        description="Current status of the record (e.g., active, inactive)",
    )
    IsAllowNegativeBalance: Optional[int] = Field(
        None,
        title="Allow Negative Balance",
        description="Indicates whether a negative leave balance is allowed",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "LeaveTypeFName": "Annual Leave",
                "LeaveTypeSName": "AL",
                "CarryForwardLimit": 10,
                "Gender": "All",
                "YearlyLimit": "20",
                "ConsiderWeeklyOff": 1,
                "ConsiderHoliday": 0,
                "MarkedAs": "Leave",
                "Description": "Regular annual leave",
                "RecordStatus": 1,
                "IsAllowNegativeBalance": -1,
            }
        }


class LeaveEntryRequestModel(BaseModel):
    LeaveTypeId: int
    FromDate: datetime = Field(datetime.now())
    ToDate: datetime = Field(datetime.now())
    Remarks: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "LeaveTypeId": 1,
                "FromDate": "3021-09-01 00:00:00",
                "ToDate": "3021-09-03 00:00:00",
                "Remarks": "Going on vacation",
            }
        }

    @model_validator(mode="after")
    def check_dates(cls, values):
        if values.FromDate > values.ToDate:
            raise ValueError("FromDate must be less than or equal to ToDate")
        return values
