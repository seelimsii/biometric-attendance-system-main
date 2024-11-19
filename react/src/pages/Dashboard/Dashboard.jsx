import WeeklyChart from "../../Components/WeeklyChart/WeeklyChart";
import TodaysHoursChart from "../../Components/TodaysHoursChart/TodaysHoursChart";
import PresentAbsent from "../../Components/PresentAbsent/PresentAbsent";
import WeeklyChart2 from "../../Components/WeeklyChart2/WeeklyChart2";
import Navbar from '../../Components/Navbar/Navbar'
import LeavesCard from '../../Components/LeavesCard/LeavesCard'

import "./Dashboard.css";
import profile from "../../assets/profile.jpg";
const Dashboard = () => {
  const Weeklydata = [
    {
      label: "Mon",
      value: 9,
    },
    {
      label: "Tue",
      value: 6,
    },
    {
      label: "Wed",
      value: 8,
    },
    {
      label: "Thu",
      value: 7,
    },
    {
      label: "Fri",
      value: 4,
    },
    {
      label: "Sat",
      value: 9,
    },
  ];
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
  const Weeklydata2 = [
    {
      label: "Completed",
      value: 22,
    },
    {
      label: "Left",
      value: 18,
    },
  ];

  return (
    <div className="flex">
        <div><Navbar/></div>

      <div className="card dashboard-container">
        <h2 className="dashboard-heading">Attendence Dashboard</h2>
        <div className="dashboard-first-row">
          <div className=" card dashboard-profile">
            <div className="dashboard-profile-image">
              <img src={profile} alt="profile" />
            </div>

            <div className="dashboard-profile-details">
              <div className="profile-detail-name">Surendra Singh</div>
              <div className="profile-detail-id">EMP356857805</div>
              <div className="profile-detail-dept">
                Department of Computer Science
              </div>
              <div className="profile-detail-campus">
                Ambedkar DSEU Shakarpur Campus- I
              </div>
            </div>
          </div>


          {/* <TodaysHoursChart data={today} /> */}
          <PresentAbsent />
        </div>
        <div className="dashboard-second-row">
          {/* <WeeklyChart data={Weeklydata} /> */}
          {/* <WeeklyChart2 data={Weeklydata2} /> */}
          <LeavesCard />
        </div>
      </div>
    </div>

  );
};

export default Dashboard;
