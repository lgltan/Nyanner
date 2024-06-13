import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';

import Login from './components/Login.jsx';
import Signup from './components/Signup.jsx';
import AdminPage from './components/AdminPage.jsx';

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route exact path="/" element={<Login/>} />
          <Route path="/sign-up" element={<Signup/>} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
