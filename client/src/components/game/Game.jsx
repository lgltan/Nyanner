import React, { useEffect, useState } from 'react';
import ChessGame from './ChessGame';
import './game.css';
import api from '../../services/api';
import { fetchToken } from '../../services/authProvider';
import { Chessboard } from 'react-chessboard';

function Game() {
  const [lobbyInfo, setLobbyInfo] = useState(null);
  const [isWaiting, setIsWaiting] = useState(true);

  const getLobby = async () => {
    try {
      const token = fetchToken();
      const response = await api.get('/lobby/info', {
        headers: {
          Content_Type: 'application/json',
          Authorization: `Bearer ${token}`
        }
      });
      setLobbyInfo(response.data);
    } catch (error) {
      console.error(error);
    }

    if ((lobbyInfo.p1_id != null) && (lobbyInfo.p2_id != null)){
      try {
        const token = fetchToken();
        const response = await api.get('/game/instantiate_moves', {
          headers: {
            Content_Type: 'application/json',
            Authorization: `Bearer ${token}`
          }
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }

  };
  
  useEffect(() => {
    const intervalId = setInterval(getLobby, 1000); // Fetch every 1 seconds

    return () => {
      clearInterval(intervalId); // Clear interval on cleanup
    };
  }, []);

  return (
    <div className="game">
      <div className="game-left-col">
        Nyanner <br />
        P1: {lobbyInfo?.p1_name ? lobbyInfo.p1_name : "Waiting"} <br />
        P2: {lobbyInfo?.p2_name ? lobbyInfo.p2_name : "Waiting"} <br />
        Lobby Code: {lobbyInfo?.lobby_code}
      </div>
      <div className="chessboard-container">
        <ChessGame />
      </div>
    </div>
  );
}

export default Game;
