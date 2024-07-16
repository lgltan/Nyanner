import React, { useState, useEffect } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { useLogout } from "../../services/authProvider";
import { fetchToken } from '../../services/authProvider.js';
import { getUserData } from '../../services/api.js';
import "../../App.css";
import "./NavBar.css";

const NavBar = () => {
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const logout = useLogout();
  const navigate = useNavigate();
  const auth = fetchToken();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userData = await getUserData(auth);
        setProfilePhoto(userData.photo.content);
      } catch (error) {
        console.error("Error fetching user data or photo:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [auth]);

  const toggleDropdown = () => {
    setDropdownVisible(!dropdownVisible);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

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
            src={`data:image/jpeg;base64,${profilePhoto}`}
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
