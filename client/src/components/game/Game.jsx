import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ChessGame from './ChessGame';
import './game.css';
import api from '../../services/api';
import { fetchToken } from '../../services/authProvider';
import { Chessboard } from 'react-chessboard';

const Game = ({inGameCheck}) => {
  const Navigate = useNavigate();
  const [lobbyInfo, setLobbyInfo] = useState(null);
  const [isWaiting, setIsWaiting] = useState(true);
  const [playerColor, setPlayerColor] = useState("white");

  useEffect(() => {
    const updatePlayerColor = async () => {
        try {
            const token = fetchToken();
            const response = await api.get('/lobby/current_player', {
            headers: {
                Authorization: `Bearer ${token}`
            }
          });
          setPlayerColor(response.data);
        } catch (error) {  
        }
      };
      updatePlayerColor();
}, []);

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
  };

  const leaveGame = async () => {
    try {
      inGameCheck(false);
      const token = fetchToken();
      const response = await api.put(`/lobby/leave_game/${lobbyInfo?.lobby_code}`, {}, {
          headers: {
              Content_Type: 'application/json',
              Authorization: `Bearer ${token}`,
          },
      });
    } catch (error) {
        console.error(error);
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
        Lobby Code: {lobbyInfo?.lobby_code}<br />
        <button onClick={leaveGame}>Leave</button>
      </div>
      <div className="chessboard-container">
        <ChessGame playerColor={playerColor}/>
      </div>
    </div>
  );
}

export default Game;
