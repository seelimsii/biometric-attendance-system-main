import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  AiOutlineHome,
  AiOutlineDashboard,
  AiOutlineUser,
  AiOutlineMenu,
} from "react-icons/ai";
import { MdOutlineSwipeLeft } from "react-icons/md";
import { BiExit } from "react-icons/bi";

function Navbar() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  const navItems = [
    { to: "/", label: "Home", icon: AiOutlineHome },
    { to: "/dashboard", label: "Dashboard", icon: AiOutlineDashboard },
    { to: "/onduty-form", label: "On Duty", icon: AiOutlineUser },
    { to: "/leave-application", label: "Leave ", icon: MdOutlineSwipeLeft },
    { to: "/about", label: "Profile", icon: AiOutlineUser },
  ];

  return (
    <div
      className={`text-blue-500 transition-width duration-500 ${
        collapsed ? "w-[74px]" : " "
      } h-screen flex flex-col`}
    >
      <div className="flex justify-between items-center p-4 border-b border-gray-200">
        <button onClick={toggleSidebar} className="h-10 text-2xl">
          <AiOutlineMenu />
        </button>
      </div>
      <nav className="flex-grow transition-all">
        {navItems.map((item, index) => (
          <Link
            key={index}
            to={item.to}
            className={`flex items-center p-4 my-1 rounded-r-full transition-all duration-300 text-blue-500 ${
              location.pathname === item.to
                ? "bg-blue-500 text-slate-50" // Set active tab background to blue and text to white
                : "hover:bg-blue-200" // Set hover background color
            }`}
          >
            <item.icon className="w-6 h-8 mx-1" />
            <span className={`ml-2 h-8 transition-all duration-300 text-xl ${collapsed ? "hidden" : ""} `}>
              {item.label}
            </span>
          </Link>
        ))}
      </nav>
      <Link
        to="/logout"
        className="flex items-center p-6 h-16 hover:bg-blue-200 border-t"
      >
        <BiExit className="w-6 h-6" />
        <span className={`ml-2 text-xl ${collapsed ? "hidden" : ""}`}>Logout</span>
      </Link>
    </div>
  );
}

export default Navbar;
