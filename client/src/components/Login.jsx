import React, { useState, useRef } from 'react';
import { IoMdEye, IoMdEyeOff } from "react-icons/io";
import { Link, useNavigate } from 'react-router-dom';
import ReCAPTCHA from "react-google-recaptcha";
import FormInput from './form/FormInput';
import '../App.css';
import './Login.css';
import './form/FormInput.css';
import api from '../services/api.js'
import {setToken} from '../services/authProvider.js'

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    rememberMe: false
  });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const toggleShowPassword = () => {
    setShowPassword(prevState => !prevState);
  };

  // const recaptcha = useRef(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/token', {
          "username": formData.username,
          "user_password": formData.password,
          "rememberMe": formData.rememberMe
      });

      // console.log('Response:', response.data);
      const token = response.data.access_token;

      try {
        const userResponse = await api.get('/auth/users/me', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const userData = userResponse.data;
        console.log('User Response:', userData);
        setToken(token);
        
        if (userData.user_type === 0) {
          // console.log('Going to Home')
          navigate('/home');
        } else {
          // console.log('Going to Admin')
          navigate('/admin');
        }
      }
      catch (error) { 
        console.log(error)
        setError('Invalid credentials');
      }
    } catch (error) {
      // console.log(error)
      setError('Invalid credentials');
    }
  };

  // with recaptcha
  // const handleSubmit = async (e) => {
  //   e.preventDefault();
  //   if(!recaptcha.current.getValue()){
  //     setError('Please Submit Captcha')
  //   }
  //   else {
  //     try {
  //       const response = await api.post('/auth/token', {
  //           "username": formData.username,
  //           "password": formData.password,
  //           "rememberMe": formData.rememberMe
  //       });
  
  //       // console.log('Response:', response.data);
  //       const token = response.data.access_token;
  
  //       try {
  //         const userResponse = await api.get('/auth/users/me', {
  //           headers: {
  //             Authorization: `Bearer ${token}`
  //           }
  //         });
  
  //         const userData = userResponse.data;
  //         console.log('User Response:', userData);
  //         setToken(token);
          
  //         if (userData.user_type === 0) {
  //           // console.log('Going to Home')
  //           navigate('/home');
  //         } else {
  //           // console.log('Going to Admin')
  //           navigate('/admin');
  //         }
  //       }
  //       catch (error) { 
  //         console.log(error)
  //         setError('Invalid credentials');
  //       }
  //     } catch (error) {
  //       // console.log(error)
  //       setError('Invalid credentials');
  //     }
  //   }
      
  // };

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
                <input 
                  type="checkbox" 
                  name="rememberMe"
                  checked={formData.rememberMe}
                  onChange={handleChange} 
                />
                <label htmlFor="rememberMe"> Remember Me </label>
              </div>
              <div className="forgot-password">
                <a href="#">Forgot Password?</a>
              </div>
            </div>
            {error && <p className="error-center">{error}</p>}
            <button className="primary-btn mt-20" type="submit">Log In</button>
            {/* <ReCAPTCHA sitekey={process.env.CAPTCHA_SITE_KEY} ref={recaptcha}/> */}
          </form>
          <div className="signup">
            <p>Don't have an account? <Link to="/signup">Sign Up</Link></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
