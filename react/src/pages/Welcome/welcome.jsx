import React,{useState} from 'react'
import { useNavigate } from 'react-router-dom';
import './welcome.css'
import logoImage from '../../assets/DSEULogo.png'

const Login = () => {
  const [formInput, setFormInput] = useState({
    password: "",
    confirmPassword: "",
    successMsg:"",
  });

  const [formError, setFormError] = useState({
    password: "",
    confirmPassword: "",
    successMsg:"",
  });

  //Handling user input chnages for form fields

  const handleUserInput = (name, value) => {
    setFormInput({
      ...formInput,
      [name]: value,
  
    });
  }

  const validateFormInput = (event) => {
    event.preventDefault()

    //Initializing an object to track input errors

    let inputError = {
      password:"",
      confirmPassword:"",
    };

    //checking if password is empty

    if(!formInput.password){
      setFormError({
        ...inputError,
        password: "Password shouldn't be empty",
      });
      return;
    }

    //checking if password and confirm password match

  if(!formInput.confirmPassword != formInput.password){
    setFormError({
      ...inputError,
      confirmPassword: "Password and confirmPassword ahould be same",
    });
    return;
  }

  }

  

  return (
    <div className='login-container'>
      <div className="card1 flex flex-col justify-center items-center">
      <img src={logoImage} alt="dseu logo" className='logo'/>
        <div className="card-header">
          <h4 className="title">
            Welcome,  
            <span> Pranchi </span> <br />
            <span className='text-base'>
              Associate Professor
            </span>

            <h4 className='text-orange-500 font-semibold'>
              Create Password
            </h4>
          </h4>
        
        </div>
        <div className="card-body">

          <form onSubmit={validateFormInput}>
            <div className="segment">
              <i className="fa fa-lock"></i>
              <input type="password"
              value={formInput.password}
              onChange={({ target }) => {
                handleUserInput(target.name, target.value)
              }}
              name='password'
              className='pinput'
              placeholder='Password'
              />
            </div>

            <p className="error-message">{formError.password}</p>

            <div className="segment">
              <i className="fa fa-lock"></i>
              <input type="confirmPassword"
            value={formInput.password}
            onChange={({ target }) => {
              handleUserInput(target.name, target.value)
            }}
            name='confirmPassword'
            className='pinput'
            placeholder='Confirm Password'
            />
            </div>

            <p className="error-message">{formError.password}</p>
            <p className="success-message">{formInput.successMsg}</p>
        
        
       <input type="submit" className='btn' value="Login" />
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login
