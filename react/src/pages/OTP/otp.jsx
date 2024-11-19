import React,{useState} from 'react'
import { useNavigate } from 'react-router-dom';
import './otp.css' 
import logoImage from '../../assets/logo.png'
// import OtpInput from "react-otp-input"
import OTPInput from 'otp-input-react';
const otp = () => {

const OtpInputCard = ({ title, resendOTP, ...rest }) => {
  const [OTP, setOTP] = useState("");
  return (
    <div
      style={{
        padding: 12,
        color: "red",
      }}
    >
      <div style={{ marginBottom: 12 }}>{title}</div>
      <OTPInput value={OTP} onChange={setOTP} {...rest} />
    </div>
  );
};

   
  return (
    <div className="otp-container">
        <div className='otp'>
            <img src={logoImage} id='i1' alt="dseu logo" />
           
           <h3>
                Delhi Skill 
                and <br />
                Enterpreneurship University
            </h3>
            <p> Govt. of Delhi</p>
            
        <div className="header">
            <div className="text">
                OTP Verification
            </div>
            <div className="text1">
                Enter OTP sent to <u> useremail@gmail.com </u>
            </div>
    <OtpInputCard
          // autoFocus
          OTPLength={6}
          otpType="any"
          disabled={false}
          inputStyles={{
            backgroundColor:"#fff",
            color: "#000",
            border: "2px solid #0072BC",
            borderRadius: "6px"
          }
          }
          // secure
        />
           
        </div>
        <br />
            <div className="submit">
                Verify OTP
            </div>
<br />
            <div className="text1">
                Request new OTP <b> Resend OTP </b>
            </div>
    </div>
    </div>
      ) }

export default otp;
