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
        <div className='game-info'>
          <h3> Lobby Code: <span className='lobbyInfo'>{lobbyInfo?.lobby_code}</span><br /> </h3>
          <h4 className='P1'> P1: <span className='lobbyInfo'>{lobbyInfo?.p1_name ? lobbyInfo.p1_name : "Waiting"}</span> </h4> 
          <h4 className='P2'> P2: <span className='lobbyInfo'>{lobbyInfo?.p2_name ? lobbyInfo.p2_name : "Waiting"}</span> </h4>
        </div>
        
        <button className="leave-game secondary-btn mt-20" onClick={leaveGame}>Leave</button>
      </div>
      <div className="chessboard-container">
        <ChessGame playerColor={playerColor}/>
      </div>
    </div>
  );
}

export default Game;
