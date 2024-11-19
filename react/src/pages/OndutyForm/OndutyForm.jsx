import React, { useState } from "react";
import Navbar from "../../Components/Navbar/Navbar";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const OndutyForm = () => {
  const [formData, setFormData] = useState({
    name: "Pranchi",
    id: "EMP12574804632",
    designation: "Associate Professor",
    onduty_type: "",
    description: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { name, id, designation, onduty_type, description } = formData;
    const jsonData = JSON.stringify(formData);
    console.log(jsonData);
    toast.success("On duty application submitted successfully");
  };

  return (
    <div className="flex">
      <Navbar />
      <div className="card leave-form-container w-full">
        <h2 className="leave-form-heading">On Duty Form</h2>
        <form onSubmit={handleSubmit}>
          <div className="leave-form-row">
            <FormInput
              label="Name"
              value={formData.name}
              readOnly
              disabled
            />
            <FormInput
              label="Employee ID"
              value={formData.id}
              readOnly
              disabled
            />
            <FormInput
              label="Designation"
              value={formData.designation}
              readOnly
              disabled
            />
          </div>
          <div className="leave-form-row">
            <div className="leave-form-input-container">
              <label>Leave Type</label>
              <select
                className="leave-form-input"
                name="onduty_type"
                value={formData.onduty_type}
                onChange={handleInputChange}
                required
              >
                <option value="">Select OD Type</option>
                <option value="Invigilation Duty">Invigilation Duty</option>
                <option value="Election Duty">Election Duty</option>
                <option value="Paper Evaluation Duty">
                  Paper Evaluation Duty
                </option>
                <option value="Census">Census</option>
                <option value="Seminar Duty">Seminar Duty</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
          <div className="leave-form-input-container leave-form-desc">
            <label>Remarks</label>
            <textarea
              className="leave-form-input"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={5}
              placeholder="If Others Describe your Duty here"
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

const FormInput = ({ label, value, readOnly, disabled }) => (
  <div className="leave-form-input-container">
    <label>{label}</label>
    <input
      className="leave-form-input"
      type="text"
      value={value}
      readOnly={readOnly}
      disabled={disabled}
    />
  </div>
);

export default OndutyForm;
