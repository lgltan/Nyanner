import React, { useState } from 'react'
import { IoMdEye, IoMdEyeOff } from "react-icons/io";
import './LogIn.css'

const LogIn = () => {
    const [showPassword, setShowPassword] = useState(false);

    const toggleShowPassword = () => {
        setShowPassword(prevState => !prevState);
    };

    return (
        <div className="container">
            <div className="login-container">
                <div className="header">
                    <h1>Welcome back!</h1>
                    <p>Log in to your account to continue</p>
                </div>
                <div className="login-form">
                    <form>
                        <div className="username">
                            <label className="input-label" name="username"> Username </label>
                            <input type="text" name="username" />
                        </div>
                        <div className='password'>
                            <label className="input-label" name="password"> Password </label>
                            <input type="text" name="password" />
                            <button type="button" className="toggle-password" onClick={toggleShowPassword}>
                                {showPassword ? <IoMdEyeOff /> : <IoMdEye />}
                            </button>
                        </div>
                        <div className="login-options">
                            <div className="remember-me">
                                <input type="checkbox" name="remember-me" />
                                <label name="remember-me"> Remember Me </label>
                            </div>
                            <div className="forgot-password">
                                <a href="#">Forgot Password?</a>
                            </div>
                        </div>
                        <button className="primary-btn">Log In</button>
                    </form>

                    <div className="signup">
                        <p>Don't have an account? <a href="#">Sign Up</a></p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default LogIn