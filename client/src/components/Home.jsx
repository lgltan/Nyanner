import React, { useState, useEffect } from 'react';
import Lobby from './game/Lobby.jsx';
import Game from './game/Game.jsx';
import { fetchToken } from '../services/authProvider.js';
import { getUserData } from '../services/api.js';
import NavBar from './misc/NavBar.jsx';
import Loading from './misc/Loading.jsx';
import api from '../services/api.js';

const Home = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [isInGame, setIsInGame] = useState(false);
    const auth = fetchToken();

    useEffect(() => {
        const fetchData = async () => {
            try {
                await getUserData(auth);
            } catch (error) {
                // console.error("Error fetching user data:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [auth]);

    useEffect(() => {
        const checkIngame = async () => {
            try {
                console.log("Updating ingame status: " + isInGame);
                const token = fetchToken();
                const response = await api.get('/lobby/ingame_check', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
              });
              setIsInGame(response.data);
            } catch (error) {
              setIsInGame(false);
            }
          };

          checkIngame();
    }, [isInGame]);

    const updateInGameStatus = (bool_ingame) => {
        console.log("Updating ingame status");
        setIsInGame(bool_ingame);
    }


    if (isLoading) {
        return <Loading />;
    }

    if (isInGame) {
        return (
            <div>
                <NavBar />
                <Game inGameCheck={updateInGameStatus}/>
            </div>
        );
    }
    else {
        return (
            <div>
                <NavBar />
                <Lobby inGameCheck={updateInGameStatus}/>
            </div>
        );
    }  
};

export default Home;
