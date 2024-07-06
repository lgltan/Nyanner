import React, { useState } from 'react';
import './lobby.css';
import WaitingRoom from './WaitingRoom'; // Ensure WaitingRoom is imported
import axios from 'axios';

const Lobby = ({ label, type, name, value, onChange, error,...props }) => {
    const [isSuccessful, setIsSuccessful] = useState(false);
    const [lobbyName, setLobbyName] = useState('');
    const [lobbyID, setLobbyID] = useState('');

    const createLobby = async () => {
        try {
            const response = await fetch('YOUR_API_ENDPOINT_FOR_CREATE_LOBBY', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: lobbyName }),
            });
            if (!response.ok) {
                throw new Error('Failed to create lobby');
            }
            setIsSuccessful(true); // Set successful state after successful API call
        } catch (error) {
            console.error(error);
        }
    };

    const joinLobby = async () => {
        try {
            const response = await fetch('YOUR_API_ENDPOINT_FOR_JOIN_LOBBY', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: lobbyID }),
            });
            if (!response.ok) {
                throw new Error('Failed to join lobby');
            }
            setIsSuccessful(true); // Set successful state after successful API call
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="lobby-container">
            {!isSuccessful ? (
                <>
                    <div className="form-input">
                        <label className="input-label" htmlFor={name}>Create Lobby</label>
                        <input
                            className="input"
                            type={type}
                            name={name}
                            value={lobbyName}
                            onChange={(e) => setLobbyName(e.target.value)}
                            {...props}
                            required
                        />
                        {error && <p className="error">{error}</p>}
                    </div>
                    <button onClick={createLobby}>Create Lobby</button>

                    <hr />

                    <div className="form-input">
                        <label className="input-label" htmlFor={name}>Join Lobby</label>
                        <input
                            className="input"
                            type={type}
                            name={name}
                            value={lobbyID}
                            onChange={(e) => setLobbyID(e.target.value)}
                            {...props}
                            required
                        />
                        {error && <p className="error">{error}</p>}
                    </div>
                    <button onClick={joinLobby}>Join Lobby</button>
                </>
            ) : (
                <WaitingRoom lobbyID={lobbyID} lobbyName={lobbyName} /> // Render WaitingRoom component if operation was successful
            )}
        </div>
    );
};

export default Lobby;