import React, { useState, useEffect } from 'react';
import Lobby from './game/Lobby.jsx';
import { fetchToken } from '../services/authProvider.js';
import { getUserData, getUserPhoto } from '../services/api.js';
import NavBar from './misc/NavBar.jsx';

const Home = () => {
    const [profilePhoto, setProfilePhoto] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const auth = fetchToken();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const userData = await getUserData(auth);
                // console.log("User data:", userData);
                // const userPhoto = await getUserPhoto(auth);
                setProfilePhoto(userData.photo.content);
            } catch (error) {
                console.error("Error fetching user data or photo:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [auth]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <NavBar profile_photo={profilePhoto} />
            <h1>Home</h1>
        </div>
    );
};

export default Home;
