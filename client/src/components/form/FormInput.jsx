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
  return (
    <div className="form-input">
      <input
        className="input"
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        {...props}
        required
      />
      <label className="input-label" htmlFor={name}>{label}</label>
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default FormInput;
