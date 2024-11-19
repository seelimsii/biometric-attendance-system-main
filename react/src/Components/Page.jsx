// Page.js
// import React from 'react';
import LeavesCard from './LeavesCard/LeavesCard';
// import CheckInOut from './Components/Check-in-out/CheckInOut';
function Page() {
  const today = [
    {
      label: "Completed",
      value: 3,
    },
    {
      label: "Left",
      value: 5,
    },
  ];
  return (
    <div className="h-screen flex justify-center items-center bg-slate-100">
      
    <LeavesCard data = {today}/>
    
    {/* <CheckInOut /> */}
    </div>
  );
}

export default Page;
