import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

import FormInput from './form/FormInput';
import ProfilePictureUpload from './form/ProfilePictureUpload';

import '../App.css';
import './Signup.css';

const Signup = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    username: '',
    password: '',
    phoneNumber: '',
    profilePhoto: null
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleProfilePhotoChange = (file, error) => {
    setFormData(prevData => ({ 
      ...prevData, 
      profilePhoto: file 
    }));
  };

  const handleSubmit = async(e) => {
    e.preventDefault();

    // console.log('before post', formData)

    // Handle form submission
    const data = new FormData();
    data.append('username', formData.username);
    data.append('password', formData.password);
    data.append('confirm_password', formData.confirmPassword);
    data.append('first_name', formData.firstName);
    data.append('last_name', formData.lastName);
    data.append('email', formData.email);
    data.append('phone_number', formData.phoneNumber);
    if (formData.profilePhoto) {
      data.append('file', formData.profilePhoto);
    }

    try {
      const response = await api.post('/auth/', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setErrors({});
      // console.log('Response:', response.data);

      // Handle successful registration (e.g., redirect to login page or show success message)
      navigate('/login')
    } catch (error) {
      // console.log(error)
      const newErrors = error.response.data.detail
      setErrors(newErrors)
    }
  };

  return (
    <div className='container'>
      <div className='register-container'>
        <div className="header">
          <h1>Sign up</h1>
        </div>
        <div className="register-form">
          <form method="POST" onSubmit={handleSubmit}>
            <div className="form-flex">
            <div className="form-left">
            <FormInput
              label="First Name"
              type="text"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              error={errors.firstName}
            />

            <FormInput
              label="Last Name"
              type="text"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              error={errors.lastName}
            />

            <FormInput
              label="E-mail"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
            />
            
            <FormInput
              label="Phone Number"
              type="text"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange}
              error={errors.phoneNumber}
            />

            <FormInput
              label="Username"
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              error={errors.username}
            />

            <FormInput
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              error={errors.password}
            />

            <FormInput
              label="Confirm Password"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              error={errors.confirmPassword}
            />
            </div>
            <div className="form-right">
              <ProfilePictureUpload
                label="Profile Photo"
                name="profilePhoto"
                accept="image/*"
                size="5"
                onChange={handleProfilePhotoChange}
                error={errors.profilePhoto}
              />
            </div>
            </div>
            {errors.general && <p className="error">{errors.general}</p>}
            <button className="primary-btn register-btn" type="submit">Register</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Signup;
