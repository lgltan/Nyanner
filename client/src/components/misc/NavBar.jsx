import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { useLogout } from "../../services/authProvider";
import "../../App.css";
import "./NavBar.css";

const NavBar = ( {profile_photo} ) => {
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const logout = useLogout();
  const navigate = useNavigate();

  const toggleDropdown = () => {
    setDropdownVisible(!dropdownVisible);
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="site-name">
          Nyanner
        </Link>
      </div>
      <div className="navbar-right">
        <button className="primary-btn mr-10" onClick={() => navigate("/game")}>
          Play Game
        </button>
        <div className="profile-container">
          <img
            src={`data:image/jpeg;base64,${profile_photo}`}
            alt="Profile"
            className="profile-image"
            onClick={toggleDropdown}
          />
          {dropdownVisible && (
            <div className="dropdown-menu">
              <Link to="/edit-profile" className="dropdown-item">
                Edit Profile
              </Link>
              <Link to="/settings" className="dropdown-item">
                Settings
              </Link>
              <button className="dropdown-item" onClick={logout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
