import React, { useState, useEffect } from "react";
import Navbar from "../../Components/Navbar/Navbar";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./LeaveForm.css";

const LeaveForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    id: "",
    designation: "",
    from_date: "",
    to_date: "",
    leave_type: "",
    description: "",
  });

  const today = new Date().toISOString().split("T")[0];

  useEffect(() => {
    setFormData((prevState) => ({
      ...prevState,
      name: person.name,
      id: person.ID,
      designation: person.Designation,
    }));
  }, []); 

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const saveFormData = (e) => {
    e.preventDefault();
    const { from_date, to_date } = formData;
    if (from_date && to_date) {
      toast.success(`Applied for leave from ${from_date} to ${to_date}`);
    } else {
      toast.error("Please select both From Date and To Date");
    }
  };

  const person = {
    name: "Pranchi",
    ID: "EMP12574804632",
    Designation: "Associate Professor",
  };

  return (
    <div className="flex">
      <div>
        <Navbar />
      </div>
      <div className="card leave-form-container w-full">
        <h2 className="leave-form-heading">Leave Application Form</h2>
        <form onSubmit={saveFormData}>
          <div className="leave-form-row">
            <div className="leave-form-input-container">
              <label>Name</label>
              <input
                className="leave-form-input"
                type="text"
                name="name"
                value={formData.name}
                readOnly
                disabled
              />
            </div>
            <div className="leave-form-input-container">
              <label>Employee ID</label>
              <input
                className="leave-form-input"
                type="text"
                name="id"
                value={formData.id}
                readOnly
                disabled
              />
            </div>
            <div className="leave-form-input-container">
              <label>Designation</label>
              <input
                className="leave-form-input"
                type="text"
                name="designation"
                value={formData.designation}
                readOnly
                disabled
              />
            </div>
          </div>
          <div className="leave-form-row">
            <div className="leave-form-input-container">
              <label>From Date</label>
              <input
                className="leave-form-input"
                type="date"
                name="from_date"
                value={formData.from_date}
                onChange={handleInputChange}
                required
                min={today}
              />
            </div>
            <div className="leave-form-input-container">
              <label>To Date</label>
              <input
                className="leave-form-input"
                type="date"
                name="to_date"
                value={formData.to_date}
                onChange={handleInputChange}
                required
                min={today}
              />
            </div>
            <div className="leave-form-input-container">
              <label>Leave Type</label>
              <select
                className="leave-form-input"
                name="leave_type"
                value={formData.leave_type}
                onChange={handleInputChange}
                required
              >
                <option value="">Select Leave Type</option>
                <option value="Sick Leave">Sick Leave</option>
                <option value="Casual Leave">Casual Leave</option>
                <option value="Paid Leave">Paid Leave</option>
                <option value="Maternity/Paternity Leave">
                  Maternity/Paternity Leave
                </option>
              </select>
            </div>
          </div>
          <div className="leave-form-input-container leave-form-desc">
            <label>Description</label>
            <textarea
              className="leave-form-input"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={5}
              required
            ></textarea>
          </div>
          <div className="leave-form-input-container">
            <button
              type="submit"
              className="bg-sky-600 hover:bg-sky-700 transition-all duration-100 px-5 py-2 rounded-full text-white"
            >
              Apply
            </button>
          </div>
        </form>
      </div>
      <ToastContainer />
    </div>
  );
};

export default LeaveForm;
