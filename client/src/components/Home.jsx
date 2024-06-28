import React, { useState } from 'react';
import { FaUser } from 'react-icons/fa';
import Lobby from './game/Lobby.jsx';
import { removeToken } from '../provider/authProvider.js';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const [activeTab, setActiveTab] = useState('profile');
    const [searchUser, setSearchUser] = useState('');
    const [searchLog, setSearchLog] = useState('');
    const navigate = useNavigate();
    
    const logout = () => {
        if(removeToken()){
            navigate('/login');
        }
        else{
            alert('Error logging out');
            console.log('Error logging out');
        }
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
                <button className="primary-btn logout" onClick={logout}>Logout</button>
            </div>
            <div className="content">
                {renderContent()}
            </div>
        </div>
    );
};

export default Home;