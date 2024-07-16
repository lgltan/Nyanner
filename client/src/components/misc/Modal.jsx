// Modal.js
import React, { useState } from "react";
import { IoMdEye, IoMdEyeOff } from "react-icons/io";
import "../form/FormInput.css";
import "./Modal.css";

const Modal = ({ isOpen, onClose, onConfirm }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [password, setPassword] = useState("");

  const toggleShowPassword = () => {
    setShowPassword((prevState) => !prevState);
  };

  const handleConfirm = () => {
    onConfirm(password);
    setPassword("");
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <h2>Confirm Changes</h2>
        <p>Please enter your password to confirm changes to your profile.</p>
        <div className="password">
          <input
            className="input"
            type={showPassword ? "text" : "password"}
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <label className="input-label" htmlFor="password">
            Password
          </label>
          <button
            type="button"
            className="toggle-password"
            onClick={toggleShowPassword}
          >
            {showPassword ? <IoMdEyeOff /> : <IoMdEye />}
          </button>
        </div>
        <div className="modal-actions">
          <button className="primary-btn" onClick={handleConfirm}>Confirm</button>
        </div>
      </div>
    </div>
  );
};

export default Modal;
