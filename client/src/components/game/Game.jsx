import React, { useEffect, useState } from 'react';
import ChessGame from './ChessGame';
import './game.css';
import api from '../../services/api';
import { fetchToken } from '../../services/authProvider';

function Game() {
  // TODO: get user id, find ongoing lobby with user id
  // TODO: on init, create move to generate default board

  const [lobbyInfo, setLobbyInfo] = useState(null);

  const getLobby = async () => {
    try {
      const token = fetchToken();
      const response = await api.get('/lobby/info', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      return response.data
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    setLobbyInfo(getLobby)
  }, []);

  return (
    <div className="game">
      <div className="game-left-col">
        Nyanner
        P1: {lobbyInfo().p1_id}
        P2: {lobbyInfo().p2_id}
        {/* insert player usernames */}
      </div>
      <div className="chessboard-container">
        <ChessGame />
      </div>
    </div>
  );
}

export default Game;