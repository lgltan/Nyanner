import React from 'react';
import './FormInput.css';

const FormInput = ({
  label,
  type,
  name,
  value,
  onChange,
  error,
  ...props
}) => {
 
  let maxLen = {}
  
  if (name === 'username') { 
    maxLen = { maxLength: '16' }
  } 
  if (name === 'firstName' || name === 'lastName' || name === 'email') {
    maxLen = { maxLength: '50' }
  }

  return (
    <div className="form-input">
      <input
        className="input"
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        {...maxLen}
        {...props}
        required
      />
      <label className="input-label" htmlFor={name}>{label}</label>
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default FormInput;
