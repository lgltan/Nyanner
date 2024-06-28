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
        console.log("error: ", newErrors)
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
    // const fileSizeLimit = parseInt(size) * 1024 * 1024; // Size limit in bytes
    // const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];

    // if (file) {
    //   if (file.size > fileSizeLimit) {
    //     setError('File size exceeds ' + size + 'MB');
    //     setPreview(null);
    //     onChange(null, 'File size exceeds size limit');
    //     return;
    //   }

    //   if (!validImageTypes.includes(file.type)) {
    //     setError('Invalid file type. Please upload an image file.');
    //     setPreview(null);
    //     onChange(null, 'Invalid file type');
    //     return;
    //   }

    //   const reader = new FileReader();
    //   reader.onloadend = () => {
    //     const img = new Image();
    //     img.onload = () => {
    //       setPreview(reader.result);
    //       setError(null);
    //       onChange(file, null);
    //     };
    //     img.onerror = () => {
    //       setError('The image file is broken.');
    //       setPreview(null);
    //       onChange(null, 'The image file is broken.');
    //     };
    //     img.src = reader.result;
    //   };
    //   reader.readAsDataURL(file);
    // } else {
    //   setError('Please upload a profile photo.');
    //   onChange(null, 'Please upload a profile photo.');
    //   setPreview(null);
    // }
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