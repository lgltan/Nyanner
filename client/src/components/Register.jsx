import React, { useState } from 'react';
import bcrypt from "bcryptjs-react";
import { IoMdEye, IoMdEyeOff } from "react-icons/io";
import FormInput from './form/FormInput';
import ProfilePictureUpload from './form/ProfilePictureUpload';

import './App.css';
import './Register.css';

const Register = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    username: '',
    password: '',
    phoneNumber: '',
    profilePhoto: null
  });
  const [errors, setErrors] = useState({});

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

  const validatePhoneNumber = (phoneNumber) => {
    const regex = /^(09|\+639)\d{9}$/;
    return regex.test(phoneNumber);
  };

  const hashPassword = async (password) => {
    const saltRounds = 10;
    try {
      const hashedPassword = await bcrypt.hash(password, saltRounds);
      return hashedPassword;
    } catch (error) {
      console.error('Error hashing password', error);
    }
  };

  const handleSubmit = async(e) => {
    e.preventDefault();
    const newErrors = {};

    if(formData.firstName.length > 50) {
      newErrors.firstName = 'First name should not exceed 50 characters'
    }

    if(formData.lastName.length > 50) {
      newErrors.lastName = 'Last name should not exceed 50 characters'
    }

    if(formData.username.length > 50) {
      newErrors.username = 'Username should not exceed 50 characters'
    }

    if(formData.email.length > 50) {
      newErrors.email = 'E-mail should not exceed 50 characters'
    }
    
    if (!validatePhoneNumber(formData.phoneNumber)) {
      newErrors.phoneNumber = 'Please enter a valid Philippine phone number.';
    }
    
    if (!formData.profilePhoto) {
      newErrors.profilePhoto = 'Please upload a profile photo.';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match.';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    else {
      setErrors({});
    }

    const hashedPassword = await hashPassword(formData.password);
    if (hashedPassword) {
      setFormData(prev => ({
        ...prev,
        password: hashedPassword
      }));

      // Handle form submission
      console.log('Form submitted', formData);
    }
  };


  return (
    <div className='container'>
      <div className='register-container'>
        <div className="header">
          <h1>Register</h1>
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
                onChange={handleChange}
                error={errors.profilePhoto}
              />
            </div>
            </div>
            <button className="primary-btn register-btn" type="submit">Register</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
