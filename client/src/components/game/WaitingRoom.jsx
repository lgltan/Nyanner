import React, { useState, useEffect } from 'react';

const WaitingRoom = ({ lobbyID, lobbyName }) => {
    const [players, setPlayers] = useState([]);

    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                const response = await fetch(`YOUR_API_ENDPOINT_TO_FETCH_PLAYERS/${lobbyID}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch players');
                }
                const data = await response.json();
                setPlayers(data.players); // Assuming the API returns an object with a players array
            } catch (error) {
                console.error(error);
                // Handle error appropriately, e.g., show an error message
            }
        };

        fetchPlayers();
    }, [lobbyID]); // Re-run the effect if lobbyID changes

    return (
        <div className="waiting-room">
            <h2>Lobby ID: {lobbyID}</h2>
            <h2>Lobby Name: {lobbyName}</h2>
            <ul>
                {players.map((player, index) => (
                    <li key={index}>{player.username}</li> // Adjust based on the actual property name in your API response
                ))}
            </ul>
        </div>
    );
};

export default WaitingRoom;