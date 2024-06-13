import React, { useState } from 'react';
import bcrypt from "bcryptjs-react";
import { IoMdEye, IoMdEyeOff } from "react-icons/io";
import { Link, useNavigate } from 'react-router-dom';
import FormInput from './form/FormInput';
import './App.css';
import './Login.css';
import './form/FormInput.css';

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const navigate = useNavigate();

  const toggleShowPassword = () => {
    setShowPassword(prevState => !prevState);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Hardcoded admin credentials for testing
  const authenticateUser = (username, password) => {
    const adminUsername = 'admin';
    const adminPassword = 'admin';
    return username === adminUsername && password === adminPassword;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (authenticateUser(formData.username, formData.password)) {
      navigate('/admin');
    } else {
      alert('Invalid credentials');
    }
    console.log('Form submitted', formData);
  };

  return (
    <div className="container">
      <div className="login-container">
        <div className="header">
          <h1>Welcome back!</h1>
          <p>Log in to your account to continue</p>
        </div>
        <div className="login-form">
          <form method="POST" onSubmit={handleSubmit}>
            <FormInput
              label="Username"
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
            />
            <div className="password">
              <input
                className='input'
                type={showPassword ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleChange}
              />
              <label className="input-label" htmlFor="password">Password</label>
              <button type="button" className="toggle-password" onClick={toggleShowPassword}>
                {showPassword ? <IoMdEyeOff /> : <IoMdEye />}
              </button>
            </div>
            <div className="login-options">
              <div className="remember-me">
                <input type="checkbox" name="remember-me" />
                <label htmlFor="remember-me"> Remember Me </label>
              </div>
              <div className="forgot-password">
                <a href="#">Forgot Password?</a>
              </div>
            </div>
            <button className="primary-btn" type="submit">Log In</button>
          </form>
          <div className="signup">
            <p>Don't have an account? <Link to="/sign-up">Sign Up</Link></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
