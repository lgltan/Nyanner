import React, { useEffect, useState } from 'react';
import ChessGame from './ChessGame';
import './game.css';
import api from '../../services/api';
import { fetchToken } from '../../services/authProvider';

function Game() {
  const [lobbyInfo, setLobbyInfo] = useState(null);
  const [isWaiting, setIsWaiting] = useState(true);

  const getLobby = async () => {
    try {
      const token = fetchToken();
      const response = await api.get('/lobby/info', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log(response.data);
      setLobbyInfo(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const intervalId = setInterval(getLobby, 5000); // Fetch every 5 seconds

    return () => {
      clearInterval(intervalId); // Clear interval on cleanup
    };
  }, []);

  useEffect(() => {
    if (lobbyInfo?.p2_id != null) {
      setIsWaiting(false);
      console.log("P2 Found.");
    }
    else {
      console.log("Waiting for P2.");
    }
  }, [lobbyInfo]);

  return (
    <div className="game">
      <div className="game-left-col">
        Nyanner <br />
        P1: {lobbyInfo?.p1_id} <br />
        P2: {lobbyInfo?.p2_id} <br />
        Lobby Code: {lobbyInfo?.lobby_code}
      </div>
      <div className="chessboard-container">
        <ChessGame />
      </div>
    </div>
  );
}

export default Game;
