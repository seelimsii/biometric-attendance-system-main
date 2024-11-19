// import React from "react";

const LeavesCard = (prop) => {
  const sourceData = prop.data;
  console.log(sourceData)
  return (
    <div className="card w-96 h-auto p-4 rounded-lg shadow-sm bg-slate-50 drop-shadow-sm">

      <div className="text-sm text-left text-[#F79219]">This Week</div>
      <div className="flex justify-evenly">
        <div className="leavesChart flex items-center justify-center border-slate-200 border-r-2 w-[45%] h-20">
            22/40
        </div>
        <div className="leavesStats w-[45%]">
          <ul className="text-[#0072BC] font-medium flex flex-col items-start ">
            <li>Total Leaves :  <span className="text-base">40</span></li>
            {/* <li>Remaining Leaves</li> */}
            <li>Late Arrival : <span className="text-base">10</span></li>
            <li>On-Duty : <span className="text-base">4</span></li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default LeavesCard;
