import React,{useState} from 'react'
import './Login.css'
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    // Here you can implement your login logic
    // For simplicity, let's just check if username and password are not empty
    if (username !== '' && password !== '') {
      setIsLoggedIn(true);
      console.log('Logged in successfully!');
    } else {
      console.log('Invalid username or password');
    }
  };
  return (
    <div className='login-container'>
      
      {!isLoggedIn ? (
        <div className='login-card'>
          <i className='fa fa-user'></i>
          <h2>Welcome, User!</h2>
          <input className='login-input'
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input className='login-input'
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button className='login-button' onClick={handleLogin}>Login</button>
        </div>
      ) : (
        <div>
          <h1>Welcome, {username}!</h1>
          <button onClick={() => setIsLoggedIn(false)}>Logout</button>
        </div>
      )}
    </div>
  )
}

export default Login
