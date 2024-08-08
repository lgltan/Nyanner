import React from 'react';
import './FormInput.css';

const FormInput = ({
  label,
  type,
  name,
  value,
  onChange,
  error,
  disabled=false,
  isRequired=false,
  ...props
}) => {
 
  let maxLen = {}
  let onFocus = {}
  let onBlur = {}
  
  if (name === 'username') { 
    maxLen = { maxLength: '16' }
  } 
  if (name === 'firstName' || name === 'lastName' || name === 'email') {
    maxLen = { maxLength: '50' }
  }
  if (name === 'birthday') {
    onFocus = {
      onFocus: (e) => {
        if (!e.target.value) {
          e.target.type = 'date';
        }
      },
    };
    onBlur = {
      onBlur: (e) => {
        if (!e.target.value) {
          e.target.type = 'text';
        }
      },
    };
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
        {...onFocus}
        {...onBlur}
        {...props}
        disabled={disabled}
        required={isRequired}
      />
      <label className="input-label" htmlFor={name}>{label}</label>
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default FormInput;
