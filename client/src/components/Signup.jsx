import React, { useState, useEffect } from 'react';
import bcrypt from "bcryptjs-react";
import FormInput from './form/FormInput';
import ProfilePictureUpload from './form/ProfilePictureUpload';

import './App.css';
import './Signup.css';

const Signup = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    username: '',
    password: '',
    phoneNumber: '',
    profilePhoto: null,
    hashedPassword: ''
  });
  const [errors, setErrors] = useState({});

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

  const validatePassword = (password, newErrors) => {
    const passwordLength = password.length;
    const hasLowercase = /[a-z]/.test(password);
    const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialCharacter = /[!@#$%^&*()_,.?":{}|<>\-]/.test(password);

    if (passwordLength < 12 || passwordLength > 32) {
      newErrors.password = 'Password must be between 12 and 32 characters long.';
    } else if (!hasLowercase) {
      newErrors.password = 'Password must contain at least one lowercase letter.';
    } else if (!hasUppercase) {
      newErrors.password = 'Password must contain at least one uppercase letter.';
    } else if (!hasNumber) {
      newErrors.password = 'Password must contain at least one number.';
    } else if (!hasSpecialCharacter) {
      newErrors.password = 'Password must contain at least one special character.';
    }
  };

  const hashPassword = async (password) => {
    const saltRounds = 10;
    try {
      const hashedPassword = await bcrypt.hash(password, saltRounds);
      setFormData(prev => ({
        ...prev,
        hashedPassword: hashedPassword
      }));
      return hashedPassword;
    } catch (error) {
      console.error('Error hashing password', error);
    }
  };

  useEffect(() => {
    if (formData.hashedPassword) {
      console.log('Form submitted', formData);
    }
  }, [formData]);

  const handleProfilePhotoChange = (file, error) => {
    if (error) {
      setErrors(prevErrors => ({ ...prevErrors, profilePhoto: error }));
    } else {
      setErrors(prevErrors => ({ ...prevErrors, profilePhoto: '' }));
      setFormData(prevData => ({ ...prevData, profilePhoto: file }));
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

    validatePassword(formData.password, newErrors);

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match.';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      console.log('Errors', newErrors);
      return;
    }
    else {
      setErrors({});
    }

    const hashedPassword = await hashPassword(formData.password);
    
    if (hashedPassword) {
      // Handle form submission
      console.log('Form submitted', formData);
    }
    console.log('Form submitted', formData.hashedPassword);
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
            <button className="primary-btn register-btn" type="submit">Register</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Signup;
