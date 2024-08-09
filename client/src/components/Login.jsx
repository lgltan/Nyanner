import React, { useState, useRef, useEffect } from 'react';
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

  const recaptcha = useRef(null);
  const [captchaKey, setCaptchaKey] = useState('');
  const hasFetchedCaptchaKey = useRef(false);
  
  useEffect(() => {
    const fetchCaptchaKey = async () => {
      try {
        const response = await api.get('/auth/recaptcha');
        setCaptchaKey(response.data.site_key);
      } catch (err) {
        setError('Failed to load CAPTCHA. Please try again later.');
      }
    };

    if (!hasFetchedCaptchaKey.current) {
      fetchCaptchaKey();
      hasFetchedCaptchaKey.current = true;
    }
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  // with recaptcha
  const handleSubmit = async (e) => {
    e.preventDefault();
    if(!recaptcha.current.getValue()){
      setError('Please Submit Captcha')
    }
    else {
      try {
        // Prepare request payload
        const request = {
          username: formData.username,
          user_password: formData.password,
          rememberMe: formData.rememberMe,
          recaptchaToken: recaptcha.current.getValue()
        };

        // Send API request with application/json header
        const response = await api.post('/auth/login', request, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
  
        const token = response.data.access_token;
  
        try {
          const userResponse = await api.get('/auth/users/me', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
  
          const userData = userResponse.data;
          // console.log('User Response:', userData);
          setToken(token);
          
          if (userData.user_type === false) {
            navigate('/home');
          } else {
            navigate('/admin');
          }
        }
        catch (error) { 
          setError('Invalid credentials');
        }
      } catch (error) {
        setError('Invalid credentials');
      }
    }
      
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
            {captchaKey && <ReCAPTCHA className="captcha mt-20" sitekey={captchaKey} ref={recaptcha}/>}
            <button className="primary-btn mt-20" type="submit">Log In</button>
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
