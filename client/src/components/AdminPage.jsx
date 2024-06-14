import React, { useState } from 'react';
import { FaUser, FaUsers, FaClipboardList } from 'react-icons/fa';
import './AdminPage.css';

const AdminPage = () => {
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
            <p>Web URLs: </p>
            <p>Bio: This is the admin bio.</p>
          </div>
        );
      case 'userlist':
        return (
          <div>
            <h2>User List</h2>
            <input
              type="text"
              placeholder="Search..."
              value={searchUser}
              onChange={(e) => setSearchUser(e.target.value)}
            />
            <button>Filter</button>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Status</th>
                    <th>Ban/Unban</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>user1</td>
                    <td>user1@example.com</td>
                    <td>Active</td>
                    <td><button>Ban</button></td>
                    
                  </tr>
                  <tr>
                    <td>user2</td>
                    <td>user2@example.com</td>
                    <td>Offline</td>
                    <td><button>Ban</button></td>
                    
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        );
      case 'logs':
        return (
          <div>
            <h2>Logs</h2>
            <input
              type="text"
              placeholder="Search logs..."
              value={searchLog}
              onChange={(e) => setSearchLog(e.target.value)}
            />
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Log ID</th>
                    <th>Message</th>
                    <th>Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>1</td>
                    <td>User logged in</td>
                    <td>2024-06-11 12:34:56</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>User logged out</td>
                    <td>2024-06-11 13:45:67</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        );
      default:
        return <div>Select a tab</div>;
    }
  };

  return (
    <div className="admin-container">
      <div className="sidebar">
        <h2>Nyanner</h2>
        <h3>Admin Dashboard</h3>
        <div className={`sidebar-item ${activeTab === 'profile' ? 'active' : ''}`} onClick={() => setActiveTab('profile')}>
          <FaUser /> Profile
        </div>
        <div className={`sidebar-item ${activeTab === 'userlist' ? 'active' : ''}`} onClick={() => setActiveTab('userlist')}>
          <FaUsers /> User List
        </div>
        <div className={`sidebar-item ${activeTab === 'logs' ? 'active' : ''}`} onClick={() => setActiveTab('logs')}>
          <FaClipboardList /> Logs
        </div>
      </div>
      <div className="content">
        {renderContent()}
      </div>
    </div>
  );
};

export default AdminPage;
