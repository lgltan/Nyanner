// Lobby.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Lobby = () => {
  const [lobbyName, setLobbyName] = useState('');
  const [lobbyID, setLobbyID] = useState('');
  const [joinLobbyID, setJoinLobbyID] = useState(''); // State for storing the lobby ID to join
  const navigate = useNavigate();

  const createLobby = async () => {
    try {
      const response = await axios.post('YOUR_API_ENDPOINT_FOR_CREATE_LOBBY', { name: lobbyName });
      setLobbyID(response.data.lobbyId); // Adjust based on your API response
      navigate(`/game/${lobbyID}`); // Navigate to the game page with the lobby ID
    } catch (error) {
      console.error(error);
    }
  };

  const joinLobby = async () => {
    try {
      const response = await axios.post('YOUR_API_ENDPOINT_FOR_JOIN_LOBBY', { id: joinLobbyID });
      navigate(`/game/${joinLobbyID}`); // Navigate to the game page with the lobby ID
    } catch (error) {
      console.error(error);
    }
  };

  const playBots = async () => {
    try {
      const response = await axios.post('API_CALL_FOR_PLAYING_AGAINST_SUNFISH', { id: lobbyID });
      navigate(`/game/${lobbyID}`); // Navigate to the game page with the lobby ID
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      {/* Input for creating a lobby */}
      <button onClick={createLobby}>Create Lobby</button>

      {/* Input for joining a lobby */}
      <input
        type="text"
        placeholder="Enter lobby ID to join"
        value={joinLobbyID}
        onChange={(e) => setJoinLobbyID(e.target.value)}
      />
      <button onClick={joinLobby}>Join Lobby</button>

      {/* Button for playing against a bot */}
      <button onClick={playBots}>Play Against Bot</button>
    </div>
  );
};

export default Lobby;