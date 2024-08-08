import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';

import { ProtectedRoute } from './services/authProvider.js';
import Login from './components/Login.jsx';
import Signup from './components/Signup.jsx';
import Home from './components/Home.jsx';
import AdminPage from './components/AdminPage.jsx';
import EditProfile from './components/EditProfile.jsx';
import Unauthorized from './components/misc/Unauthorized.jsx';

import { fetchToken } from './services/authProvider.js';
import BrokenPage from './components/misc/BrokenPage.jsx';

const App = () => {
  const isLoggedIn = !!fetchToken();

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={
            isLoggedIn ? <Navigate to="/home" /> : <Navigate to="/login" />
          } />
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<Signup/>} />
          <Route path="/home" element={
              <ProtectedRoute isAdminRoute={false}>
                <Home />
              </ProtectedRoute>
                  } />
          <Route path="/admin" element={
              <ProtectedRoute isAdminRoute={true}>
                <AdminPage />
              </ProtectedRoute>
                  } />
          <Route path="/edit-profile" element={
              <ProtectedRoute isAdminRoute={false}>
                <EditProfile />
              </ProtectedRoute>
                  } />
          <Route path="/oops" element={<Unauthorized />} />
          <Route path="/settings" element={<Unauthorized />} />
          <Route path="/oops2" element={<BrokenPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
