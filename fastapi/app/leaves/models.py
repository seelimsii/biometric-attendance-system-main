from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LeaveEntry(BaseModel):
    LeaveTypeId: int = Field(
        default=0,
        description="Identifier for the type of leave. Default value is 0.",
        title="Leave Type ID",
        ge=0,
    )
    LeaveStatus: Optional[str] = Field(
        default="Pending",  # TODO: Change to "Pending" after testing
        description="Status of the leave entry.",
        title="Leave Status",
        max_length=255,
    )
    EmployeeId: int = Field(
        description="Identifier for the employee who requested the leave.",
        title="Employee ID",
    )
    FromDate: datetime = Field(
        description="Start date of the leave. It must be in YYYY-MM-DD HH:MM:SS format.",
        title="From Date",
        gt=datetime.now(),
    )
    ToDate: datetime = Field(
        description="End date of the leave. It must be in YYYY-MM-DD HH:MM:SS format.",
        title="To Date",
        gt=datetime.now(),
    )
    IsApproved: int = Field(
        default=0,
        description="Flag indicating if the leave is approved or not. It must be 0 (not approved) or 1 (approved).",
        title="Is Approved",
    )
    ApprovedBy: Optional[str] = Field(
        default=None,
        description="Employee who approved the leave. It must not exceed 255 characters.",
        title="Approved By",
        max_length=255,
    )
    Remarks: Optional[str] = Field(
        default=None,
        description="Remarks for the leave entry. It must not exceed 4000 characters.",
        title="Remarks",
        max_length=4000,
    )
    LastModifiedBy: Optional[str] = Field(
        description="Employee who last modified the entry. It must not exceed 50 characters.",
        title="Last Modified By",
        max_length=50,
    )
    CreatedDate: Optional[datetime] = Field(
        description="Date and time when the entry was created. It must be in YYYY-MM-DD HH:MM:SS format.",
        title="Created Date",
    )
    LastModifiedDate: Optional[datetime] = Field(
        description="Date and time when the entry was last modified. It must be in YYYY-MM-DD HH:MM:SS format.",
        title="Last Modified Date",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "LeaveTypeId": 1,
                "LeaveStatus": "Pending",
                "EmployeeId": 1,
                "FromDate": "2021-09-01 00:00:00",
                "ToDate": "2021-09-03 00:00:00",
                "IsApproved": 0,
                "ApprovedBy": "Admin",
                "Remarks": "Annual leave request",
                "LastModifiedBy": "Admin",
                "CreatedDate": "2021-09-01 00:00:00",
                "LastModifiedDate": "2021-09-01 00:00:00",
            }
        }
