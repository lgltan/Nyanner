import React, { useState, useEffect } from 'react';
import Lobby from './game/Lobby.jsx';
import { fetchToken } from '../services/authProvider.js';
import { getUserData } from '../services/api.js';
import NavBar from './misc/NavBar.jsx';
import Loading from './misc/Loading.jsx';

const Home = () => {
    const [isLoading, setIsLoading] = useState(true);
    const auth = fetchToken();

    useEffect(() => {
        const fetchData = async () => {
            try {
                await getUserData(auth);
            } catch (error) {
                console.error("Error fetching user data:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [auth]);

    if (isLoading) {
        return <Loading />;
    }

    return (
        <div>
            <NavBar />
            <h1>Home</h1>
        </div>
    );
};

export default Home;
