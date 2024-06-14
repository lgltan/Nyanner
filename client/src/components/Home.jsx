import React, { useState } from 'react';
import { FaUser } from 'react-icons/fa';
import Lobby from 'game/Lobby.jsx';

const Home = () => {
    const [activeTab, setActiveTab] = useState('profile');
    const [searchUser, setSearchUser] = useState('');
    const [searchLog, setSearchLog] = useState('');

    const renderContent = () => {
        switch (activeTab) {
            case 'profile':
                return (
                    <div>
                        <h2>User Profile</h2>
                        <img src="profile-pic-url" alt="Profile" />
                        <p>Username: admin</p>
                        <p>Email: admin@example.com</p>
                        <p>Web URLs: <a href="https://example.com">https://example.com</a></p>
                        <p>Bio: This is the admin bio.</p>
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