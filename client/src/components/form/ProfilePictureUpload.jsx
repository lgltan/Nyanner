import React, { useState, useEffect } from 'react';
import './ProfilePictureUpload.css';
import api from '../../services/api';

const ProfilePictureUpload = ({ label, name, accept, size, onChange, error: externalError }) => {
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(externalError);
  const [file, setFile] = useState(null);

  useEffect(() => {
    setError(externalError);
  }, [externalError]);

  const handleChange = async(e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile) {
      try {
        const data = new FormData();
        data.append('file', selectedFile);

        const response = await api.post('/auth/uploadfile', data, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        setError(null);
        setPreview(URL.createObjectURL(selectedFile));
        onChange(selectedFile, null);
      } 
      catch (error) {
        const newErrors = error.response.data.detail
        // console.log("error: ", newErrors)
        setError(newErrors? newErrors : "An error occurred")
        setPreview(null);
        onChange(null, newErrors);
        setFile(null);
      }
    }
    else {  
      setError('Please upload a profile photo.');
      setPreview(null);
      onChange(null, 'Please upload a profile photo.');
      setFile(null);
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
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default ProfilePictureUpload;