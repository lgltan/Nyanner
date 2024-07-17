import React, { useState } from 'react';
import './lobby.css';
import api from '../../services/api';
import { useNavigate } from 'react-router-dom';

const Lobby = ({ label, type, name, value, onChange, error, ...props }) => {
    const [lobbyCode, setLobbyCode] = useState('');
    const navigate = useNavigate();

    const createLobby = async () => {
        try {
            const response = await api.post('/lobby');
            navigate(`/game`); // Navigate to the game page with the lobby ID
        } catch (error) {
            console.error(error);
        }
    };

    const joinLobby = async () => {
        try {
            const response = await api.post('/lobby/join', { access_code: lobbyCode });
            navigate(`/game`); // Navigate to the game page with the lobby ID
        } catch (error) {
            console.error(error);
        }
    };

    const playBots = async () => {
        try {
            const response = await api.post('API_CALL_FOR_PLAYING_AGAINST_SUNFISH');
            navigate(`/game`); // Navigate to the game page with the lobby ID
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="lobby-container">
                    <button onClick={createLobby}>Create Lobby</button>
                    <hr />
                    <div className="form-input">
                        <label className="input-label" htmlFor={name}>Join Lobby</label>
                        <input
                            className="input"
                            type={type}
                            name={name}
                            value={lobbyCode}
                            onChange={(e) => setLobbyCode(e.target.value)}
                            {...props}
                            required
                        />
                        {error && <p className="error">{error}</p>}
                    </div>
                    <button onClick={joinLobby}>Join Lobby</button>
                    <hr />
                    <button onClick={playBots}>Play Bots</button>
                    
        </div >
    );
};

export default Lobby;