create_leave_type_stmt = """
    INSERT INTO LeaveTypes (
        LeaveTypeFName,
        LeaveTypeSName,
        CarryForwardLimit,
        Gender,
        YearlyLimit,
        ConsiderWeeklyOff,
        ConsiderHoliday,
        MarkedAs,
        Description,
        RecordStatus,
        IsAllowNegativeBalance
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

get_leaves_type_stmt = """
    SELECT
        LeaveTypeFName,
        LeaveTypeSName,
        CarryForwardLimit,
        Gender,
        YearlyLimit,
        ConsiderWeeklyOff,
        ConsiderHoliday,
        MarkedAs,
        Description,
        RecordStatus,
        IsAllowNegativeBalance
    FROM LeaveTypes
    """

update_leave_type_stmt = """
    UPDATE LeaveTypes
    SET
        LeaveTypeFName = ?,
        LeaveTypeSName = ?,
        CarryForwardLimit = ?,
        Gender = ?,
        YearlyLimit = ?,
        ConsiderWeeklyOff = ?,
        ConsiderHoliday = ?,
        MarkedAs = ?,
        Description = ?,
        RecordStatus = ?,
        IsAllowNegativeBalance = ?
    WHERE
        LeaveTypeID = ?;
    """

create_leave_stmt = """
    INSERT INTO LeaveEntries (
        LeaveTypeId,
        LeaveStatus,
        EmployeeId,
        FromDate,
        ToDate,
        IsApproved,
        ApprovedBy,
        Remarks,
        LastModifiedBy,
        CreatedDate,
        LastModifiedDate
    )
    OUTPUT INSERTED.*
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
