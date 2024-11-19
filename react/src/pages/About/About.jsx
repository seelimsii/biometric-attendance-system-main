import React from "react";
import Navbar from "../../Components/Navbar/Navbar";
import { AiOutlineUser } from "react-icons/ai";

const About = () => {
  const userDetails = {
    name: "Pranchi",
    jobRole: "Associate Professor",
    email: "pranchi@dseu.ac.in",
  };
  return (
    <div className="flex">
      <div>
        <Navbar />
      </div>
      <div className="flex justify-center items-center w-full">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col items-center">
            <AiOutlineUser alt="User" className="w-24 h-24 rounded-full mb-4" />
            <h1 className="text-2xl font-bold mb-2">{userDetails.name}</h1>
            <p className="text-gray-500">{userDetails.jobRole}</p>
          </div>
          <div className="mt-8">
            <h2 className="text-lg font-bold mb-4">Personal Information</h2>
            <div className="flex flex-col space-y-4">
              <div>
                <p className="font-bold">Email:</p>
                <p>{userDetails.email}</p>
              </div>
              {/* Add more personal information here */}
            </div>
          </div>
          {/* Add more sections for settings, additional details, etc. */}
        </div>
      </div>
    </div>
  );
};

export default About;
