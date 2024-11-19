
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SignIn.css";
import logoImage from "../../assets/logo.png";

const SignIn = () => {
  return (
    <div className="signup-container">
      <div className="signup">
        <div className="header">
          <img src={logoImage} id="i1" alt="dseu logo" />

            <h3>
                Delhi Skill 
                and <br />
                Enterpreneurship University
            </h3>
            <p> Govt. of Delhi</p>

          <div className="text">Sign In</div>
          <div className="inputs">
            <div className="input">
              <i className="fa fa-envelope"></i>
              <input type="text" placeholder="Email Address" />
            </div>
          </div>
        </div>
        <br />
        <div className="submit">Generate OTP</div>
      </div>
    </div>
  );
};

export default SignIn