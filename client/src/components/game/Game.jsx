import React, { useEffect, useState } from 'react';
import ChessGame from './ChessGame';
import './game.css';
import api from '../../services/api';
import { fetchToken } from '../../services/authProvider';

function Game() {
  const [lobbyInfo, setLobbyInfo] = useState(null);
  const [isWaiting, setIsWaiting] = useState(true); // State to control fetching

  const getLobby = async () => {
    try {
      const token = fetchToken();
      const response = await api.get('/lobby/info', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setLobbyInfo(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const intervalId = setInterval(getLobby, 5000); // Fetch every 5 seconds
    if (lobbyInfo?.p2_id != null) {
      setIsWaiting(false);
      console.log("P2 Found.");
    }

    return () => {
      clearInterval(intervalId); // Clear interval on cleanup
    };
  }, [isWaiting]); // Depend on isWaiting state

  return (
    <div className="game">
      <div className="game-left-col">
        Nyanner
        P1: {lobbyInfo?.p1_id}
        P2: {lobbyInfo?.p2_id}
        {/* insert player usernames */}
      </div>
      <div className="chessboard-container">
        <ChessGame />
      </div>
  </div>
  );
}

export default Game;
