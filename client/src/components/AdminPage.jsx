import React, { useState, useEffect, useCallback } from 'react';
import { FaUser, FaUsers, FaClipboardList } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import './AdminPage.css';
import { useLogout, fetchToken } from '../services/authProvider.js';
import api from '../services/api.js';

const AdminPage = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [userData, setUserData] = useState({});
  const [users, setUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [searchUser, setSearchUser] = useState('');
  const [searchLog, setSearchLog] = useState('');
  const navigate = useNavigate();

  const fetchUserData = useCallback(async () => {
    try {
      const token = fetchToken();
      const response = await api.get('/auth/users/me', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setUserData(response.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
      navigate('/login');
    }
  }, [navigate]);

  const fetchAllUsers = useCallback(async () => {
    try {
      const token = fetchToken();
      const response = await api.get('/admin/users', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching all users:', error);
    }
  }, []);

  const fetchLogs = useCallback(async () => {
    try {
      const token = fetchToken();
      const response = await api.get('/admin/logs', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setLogs(response.data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  }, []);

  // const handleBanUser = async (userId, duration) => {
  //   try {
  //     const token = fetchToken();
  //     await api.post(`/admin/ban/${userId}`, { duration }, {
  //       headers: {
  //         Authorization: `Bearer ${token}`
  //       }
  //     });
  //     fetchAllUsers(); // Refresh user list
  //   } catch (error) {
  //     console.error('Error banning user:', error);
  //   }
  // };

  // const handleUnbanUser = async (userId) => {
  //   try {
  //     const token = fetchToken();
  //     await api.post(`/admin/unban/${userId}`, {}, {
  //       headers: {
  //         Authorization: `Bearer ${token}`
  //       }
  //     });
  //     fetchAllUsers(); // Refresh user list
  //   } catch (error) {
  //     console.error('Error unbanning user:', error);
  //   }
  // };

  useEffect(() => {
    if (activeTab === 'profile') {
      fetchUserData();
    } else if (activeTab === 'userlist') {
      fetchAllUsers();
    } else if (activeTab === 'logs') {
      fetchLogs();
    }
  }, [activeTab, fetchUserData, fetchAllUsers, fetchLogs]);

  const logout = useLogout();

  const renderContent = () => {
    switch (activeTab) {
      case 'profile':
        return (
          <div>
            <h2>User Profile</h2>
            <p>Username: {userData.username}</p>
            <p>Email: {userData.email}</p>
            <p>First Name: {userData.first_name}</p>
            <p>Last Name: {userData.last_name}</p>
            <p>Phone Number: {userData.phone_number}</p>
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
                  {users.map((user) => (
                    <tr key={user.user_id}>
                      <td>{user.username}</td>
                      <td>{user.email}</td>
                      <td>{user.ban_bool ? 'Banned' : 'Active'}</td>
                      <td>
                        {/* {user.ban_bool ? (
                          <button onClick={() => handleUnbanUser(user.user_id)}>Unban</button>
                        ) : (
                          <button onClick={() => handleBanUser(user.user_id, 30)}>Ban</button>
                        )} */}
                      </td>
                    </tr>
                  ))}
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
                  {logs.map((log) => (
                    <tr key={log.admin_log_id}>
                      <td>{log.admin_log_id}</td>
                      <td>{log.admin_description}</td>
                      <td>{log.admin_timestamp}</td>
                  </tr>
                  ))}
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
        <div className="sidebar-item" onClick={logout}>
          Logout
        </div>
      </div>
      <div className="content">
        {renderContent()}
      </div>
    </div>
  );
};

export default AdminPage;
