import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';

import { ProtectedRoute } from './provider/authProvider.js';
import Login from './components/Login.jsx';
import Signup from './components/Signup.jsx';
import Home from './components/Home.jsx';
import AdminPage from './components/AdminPage.jsx';
import Lobby from './components/game/Lobby.jsx';

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
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
          <Route path="/lobby" element={
              // <ProtectedRoute isAdminRoute={false}>
                <Lobby />
              // </ProtectedRoute>
                  } />
          <Route path="/unauthorized" element={<h1>Unauthorized</h1>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
