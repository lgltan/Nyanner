import React, { useState, useEffect } from "react";
import Lobby from "./game/Lobby.jsx";
import { fetchToken } from "../services/authProvider.js";
import { getUserData } from '../services/api.js';
import NavBar from "./misc/NavBar.jsx";
import { useNavigate } from "react-router-dom";
import FormInput from "./form/FormInput.jsx";
import ProfilePictureUpload from "./form/ProfilePictureUpload.jsx";
import api from "../services/api.js";
import Modal from "./misc/Modal.jsx";
import Loading from "./misc/Loading.jsx";
import "../App.css";
import "./EditProfile.css";

const Home = () => {
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const auth = fetchToken();

  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    username: "",
    confirm_password: "",
    phoneNumber: "",
    birthday: "",
    profilePhoto: null,
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleConfirm = async (password) => {
    // Handle form submission
    const data = new FormData();
    data.append("first_name", formData.firstName);
    data.append("last_name", formData.lastName);
    data.append("phone_number", formData.phoneNumber);
    data.append("birthday", formData.birthday);
    data.append("confirm_password", password);
    if (typeof formData.profilePhoto === 'object') {
      data.append("file", formData.profilePhoto);
    }

    try {
      const response = await api.put("/auth/edit/me", data, {
        headers: {
          "Content-Type": "multipart/form-data",
          "Authorization": `Bearer ${auth}`,
        },
      });
      setErrors({});
      window.location.reload();
    } catch (error) {
      const newErrors = error.response.data.detail;
      setErrors(newErrors);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userData = await getUserData(auth);
        // const userPhoto = await getUserPhoto(auth);
        setProfilePhoto(userData.photo_content);
        setFormData({
          firstName: userData.first_name,
          lastName: userData.last_name,
          email: userData.email,
          username: userData.username,
          phoneNumber: userData.phone_number,
          birthday: userData.birthday,
          profilePhoto: `data:image/jpeg;base64,${userData.photo.content}`,
        });
      } catch (error) {
        // console.error("Error fetching user data or photo:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [auth]);

  if (isLoading) {
    return <Loading />;
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleProfilePhotoChange = (file, error) => {
    setFormData((prevData) => ({
      ...prevData,
      profilePhoto: file,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsModalOpen(true);
  };

  return (
    <div>
      <NavBar profile_photo={profilePhoto} />
      <div className="edit-container">
        <div className="header">
          <h1>Edit Profile</h1>
        </div>
        <div className="register-form">
          <form method="PUT" onSubmit={handleSubmit}>
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
                  disabled={true}
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
                  label="Birthday"
                  type="date"
                  name="birthday"
                  value={formData.birthday}
                  onChange={handleChange}
                  error={errors.birthday}
                />

                <FormInput
                  label="Username"
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  error={errors.username}
                  disabled={true}
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
                  value={formData.profilePhoto}
                />
              </div>
            </div>
            {errors.general && <p className="error">{errors.general}</p>}
            <button className="primary-btn register-btn mt-20" type="submit">
              Save
            </button>
          </form>
          <Modal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            onConfirm={handleConfirm}
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
