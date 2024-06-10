import React, { useState, useEffect } from 'react';
import './ProfilePictureUpload.css';

const ProfilePictureUpload = ({ label, name, accept, size, error: externalError, onChange }) => {
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(externalError);

  const handleChange = (e) => {
    const file = e.target.files[0];
    const fileSizeLimit = parseInt(size) * 1024 * 1024; // 5MB size limit

    if (file && file.size > fileSizeLimit) {
      setError('File size exceeds ' + size + 'MB')
      setPreview(null)
      onChange({ target: { name, value: null } }, 'File size exceeds size limit');
    } else {
      if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
          setPreview(reader.result);
        };
        setError(null);
        onChange(e, null);
        reader.readAsDataURL(file);
      } else {
        setError('Please upload a profile photo.')
        onChange(e, 'Please upload a profile photo.');
        setPreview(null);
      }
    }
  };

  return (
    <div className="profile-picture-upload">
      <label className="upload-label" htmlFor={name}>{label}</label>
      <div className="profile-picture-preview">
        {preview ? (
          <img src={preview} alt="Profile Preview" className="profile-picture" />
        ) : (
          <div className="placeholder">No Image</div>
        )}
      </div>
      <input
        className="upload-input"
        type="file"
        name={name}
        accept={accept}
        onChange={handleChange}
      />
      <p className="upload-info">File size limit: {size}MB</p>
      {error && <p className="error"> {error} </p>}
      
    </div>
  );
};

export default ProfilePictureUpload;
