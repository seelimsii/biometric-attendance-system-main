import { useState } from "react";
import "./LeaveManagement.css";
import profile from "../../assets/profile.jpg";
import { Link } from "react-router-dom";
import Navbar from "../../Components/Navbar/Navbar";

const LeaveManagement = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };
  function HolidayCard({ holiday }) {
    return (
      <div className="card">
        <h3>{holiday.name}</h3>
        <p>Date: {holiday.date}</p>
      </div>
    );
  }

  function HolidayList({ holidays }) {
    return (
      <div className="holiday-list">
        {holidays.map((holiday, index) => (
          <HolidayCard key={index} holiday={holiday} />
        ))}
      </div>
    );
  }

  const currentDate = new Date();
  const month = (currentDate.getMonth() + 1).toString().padStart(2, "0");
  const [selectedMonth, setSelectedMonth] = useState(month);

  const handleChange = (event) => {
    setSelectedMonth(event.target.value);
  };

  const holidaysData = [
    { name: "New Year's Day", date: "2024-01-01" },
    { name: "Martin King Jr. Day", date: "2024-01-15" },
    { name: "Presidents' Day", date: "2024-02-19" },
    { name: "Presidents' Day", date: "2024-02-19" },
    { name: "Presidents' Day", date: "2024-02-19" },
    { name: "Presidents' Day", date: "2024-02-19" },
    { name: "St. Patrick's Day", date: "2024-03-17" },
    { name: "April Fools' Day", date: "2024-04-01" },
    { name: "Easter Sunday", date: "2024-04-21" },
    { name: "Easter Sunday", date: "2024-04-21" },
    { name: "Easter Sunday", date: "2024-04-21" },
    { name: "Mother's Day", date: "2024-05-12" },
    { name: "Memorial Day", date: "2024-05-27" },
    { name: "Memorial Day", date: "2024-05-27" },
    { name: "Memorial Day", date: "2024-05-27" },
    { name: "Father's Day", date: "2024-06-16" },
    { name: "Labor Day", date: "2024-09-02" },
    { name: "Columbus Day", date: "2024-10-14" },
    { name: "Halloween", date: "2024-10-31" },
    { name: "Veterans Day", date: "2024-11-11" },
    { name: "Thanksgiving Day", date: "2024-11-28" },
    { name: "Christmas Day", date: "2024-12-25" },
    { name: "Christmas Day", date: "2024-12-25" },
    { name: "Christmas Day", date: "2024-12-25" },
  ];
  const leaves = [
    {
      id: "1",
      type: "Sick Leave",
      to: "25-05-24",
      from: "28-05-24",
      status: "Pending",
      description: "lorem nviabj vbrusiav ufisabv uvis",
    },
    {
      id: "2",
      type: "Casual Leave",
      to: "12-07-24",
      from: "13-07-24",
      status: "Rejected",
      description: "lorem nviabj vbrusiav ufisabv uvis",
    },
    {
      id: "3",
      type: "Paid Leave",
      to: "05-04-24",
      from: "07-04-24",
      status: "Accepted",
      description: "lorem nviabj vbrusiav ufisabv uvis",
    },
    {
      id: "4",
      type: "Casual Leave",
      to: "15-03-24",
      from: "15-03-24",
      status: "Rejected",
      description: "lorem nviabj vbrusiav ufisabv uvis",
    },
    {
      id: "5",
      type: "Sick Leave",
      to: "25-05-24",
      from: "25-05-24",
      status: "Accepted",
      description: "lorem nviabj vbrusiav ufisabv uvis",
    },
  ];

  const months = [
    { value: "01", label: "January" },
    { value: "02", label: "February" },
    { value: "03", label: "March" },
    { value: "04", label: "April" },
    { value: "05", label: "May" },
    { value: "06", label: "June" },
    { value: "07", label: "July" },
    { value: "08", label: "August" },
    { value: "09", label: "September" },
    { value: "10", label: "October" },
    { value: "11", label: "November" },
    { value: "12", label: "December" },
  ];

  const filteredHolidays = holidaysData.filter((holiday) =>
    holiday.date.startsWith(`2024-${selectedMonth}`)
  );
  return (
    <>
      <Navbar />
      <div className="leave-managment">
        <h2 className="leave-managment-heading">Leave Managment</h2>
        <div className="leave-container">
          <div className="leave-column">
            <div className="card leave-profile">
              <div className="leave-profile-image">
                <img src={profile} alt="profile" />
              </div>

              <div className="leave-profile-details">
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
            <div className="card leave-take-section">
              <div className="leave-take-buttons">
                <Link to="/leave-application">
                  <button>Apply for Leave</button>
                </Link>

                <button>&#8634;</button>
              </div>
              <div className="leave-take-cards">
                {leaves.map((item) => (
                  <div className="card leave-take-card" key={item.id}>
                    <div className="accordian-header" onClick={toggleAccordion}>
                      <p className="leave-type">{item.type}</p>
                      <p className={`leave-status leave-status-${item.status}`}>
                        {item.status}
                      </p>
                      <p className="leave-date">
                        {item.from} to {item.to}
                      </p>

                      {isOpen ? (
                        <i className="fa fa-sort-asc"></i>
                      ) : (
                        <i className="fa fa-sort-desc"></i>
                      )}
                    </div>
                    {isOpen && (
                      <div className="accordion-content">
                        <p>{item.description}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="leave-column">
            <div className="card month-holidays">
              <h2>Holidays and Leaves</h2>
              <select
                className="holiday-month-selector"
                value={selectedMonth}
                onChange={handleChange}
              >
                {months.map((month) => (
                  <option key={month.value} value={month.value}>
                    {month.label}
                  </option>
                ))}
              </select>
              <HolidayList holidays={filteredHolidays} />
            </div>
            <div className=" card leave-record-container">
              <h2>Your Leaves</h2>
              <div className="leave-record-cards">
                <div className="card leave-record-card">
                  <h3 className="leave-record-heading">Sick Leave</h3>
                  <div className="leave-record-no">
                    3<span>/5</span>
                  </div>
                </div>
                <div className="card leave-record-card">
                  <h3 className="leave-record-heading">Casual Leave</h3>
                  <div className="leave-record-no">
                    2<span>/8</span>
                  </div>
                </div>
                <div className="card leave-record-card">
                  <h3 className="leave-record-heading">Paid Leave</h3>
                  <div className="leave-record-no">
                    6<span>/10</span>
                  </div>
                </div>
                <div className="card leave-record-card">
                  <h3 className="leave-record-heading">Others</h3>
                  <div className="leave-record-no">0</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default LeaveManagement;
