import React, { useState } from 'react';
import { FaUser } from 'react-icons/fa';
import Lobby from './game/Lobby.jsx';
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./authProvider";

const Home = () => {
    const [activeTab, setActiveTab] = useState('profile');
    const [searchUser, setSearchUser] = useState('');
    const [searchLog, setSearchLog] = useState('');

    const { token } = useAuth();

    if (!token) {
        // If not authenticated, redirect to the login page
        return <Navigate to="/" />;
    }

    const renderContent = () => {
        switch (activeTab) {
            case 'profile':
                return (
                    <div>
                        <h2>User Profile</h2>
                        <img src="profile-pic-url" alt="Profile" />
                        <p>Username: username</p>
                        <p>Email: user@example.com</p>
                        <p>Web URLs: </p>
                        <p>Bio: This is the user's bio.</p>
                    </div>
                );
            case 'lobby':
                return (
                    <Lobby />
                );
            default:
                return <div></div>;
        }
    };

    return (
        <div className="admin-container">
            <div className="sidebar">
                <h2>Nyanner</h2>
                <h3>Home</h3>
                <div className={`sidebar-item ${activeTab === 'profile' ? 'active' : ''}`} onClick={() => setActiveTab('profile')}>
                    <FaUser /> Profile
                </div>
                <div className={`sidebar-item ${activeTab === 'lobby' ? 'active' : ''}`} onClick={() => setActiveTab('lobby')}>
                    <FaUser /> Lobby
                </div>
            </div>
            <div className="content">
                {renderContent()}
            </div>
        </div>
    );
};

export default Home;