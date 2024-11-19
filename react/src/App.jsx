import './App.css'
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
// import { Chart as ChartJS } from 'chart.js/auto'
import Home from './pages/Home/Home'
import About from './pages/About/About'
import Event from './pages/Event/Event'
import SignIn from './pages/SignIn/SignIn'
import ContactUs from './pages/Contact Us/ContactUs'
import Dashboard from './pages/Dashboard/Dashboard';
import LeaveForm from './pages/LeaveForm/LeaveForm';
import LeaveManagement from './pages/LeaveManagement/LeaveManagement';
import Otp from './pages/OTP/otp'
import Welcome from './pages/Welcome/welcome'
import OndutyForm from './pages/OndutyForm/OndutyForm';

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/about" element={<About/>} />
          <Route path="/events" element={<Event/>} />
          <Route path="/signin" element={<SignIn/>} />
          <Route path="/contact" element={<ContactUs/>} />
          <Route path="/dashboard" element={<Dashboard/>} />
          <Route path='/leave-management' element={<LeaveManagement/>}/>
          <Route path="/welcome" element={<Welcome/>}/>
          <Route path="/otp" element={<Otp/>}/>
          <Route path="/leave-application" element={<LeaveForm/>} />
          <Route path='/onduty-form' element={<OndutyForm/>}/>
        </Routes>
    </Router>
    </>
  )
}

export default App
