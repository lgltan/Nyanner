// Roughly based on https://dev.to/oyedeletemitope/login-authentication-with-react-and-fastapi-397b

import { useState, useEffect } from "react";
import { useLocation, Navigate } from "react-router-dom"
import api from "../services/api"

export const USER_TYPES = {
    REGULAR: 0,
    ADMIN: 1,
  };

export const setToken = (token)=>{
    localStorage.setItem('token', token)
}

export const fetchToken = (token)=>{
    return localStorage.getItem('token')
}

export const removeToken = (token)=>{
    if (localStorage.getItem('token') === null)
        return false;
    localStorage.removeItem('token');
    return true;
}

export function ProtectedRoute({ isAdminRoute = false, children }) {
    const [loading, setLoading] = useState(true);
    const [isAuthorized, setIsAuthorized] = useState(false);
    const auth = fetchToken();
    const location = useLocation();
  
    useEffect(() => {
      const checkAuthorization = async () => {
        if (!auth) {
          setLoading(false);
          return;
        }
  
        try {
          const userResponse = await api.get('/auth/users/me', {
            headers: {
              Authorization: `Bearer ${auth}`,
            },
          });
  
          const userData = userResponse.data;
          const user_type = userData.user_type;
  
          if ((isAdminRoute && user_type === USER_TYPES.ADMIN) || 
              (!isAdminRoute && user_type === USER_TYPES.REGULAR)) {
            setIsAuthorized(true);
          }
        } catch (error) {
          console.error('Error fetching user data:', error);
        } finally {
          setLoading(false);
        }
      };
  
      checkAuthorization();
    }, [auth, isAdminRoute]);
  
    if (loading) {
      return <div>Loading...</div>; // or a spinner component
    }
  
    if (!auth) {
      return <Navigate to='/login' state={{ from: location }} />;
    }
  
    if (!isAuthorized) {
      return <Navigate to='/unauthorized' />;
    }
  
    return children;
  }