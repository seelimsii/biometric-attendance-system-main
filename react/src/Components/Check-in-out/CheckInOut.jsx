// import React from 'react'
import { TbClockCheck, TbClockCancel} from "react-icons/tb";
function CheckInOut() {
  return (
    <div className='flex justify-evenly'>
      <div>
        <TbClockCheck />
        Check-in
      </div>
      <div>
        {/* <PiClockUserFill /> */}
        Completed
      </div>
      <div>
        <TbClockCancel />
        Check-out
      </div>
    </div>
  )
}

export default CheckInOut
