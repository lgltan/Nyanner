// page for the game proper

// main loop
// - check db for game state - current board, current phase
// - - possible actions: [move unit, purchase unit, roll for new units, purchase xp]
// - submit action log to backend

// backend
// - figure out a way to sync actual chessboard and timings

import React, { useEffect, useRef } from 'react';
import Chessboard from './Chessboard';
import { io } from "socket.io-client"; // Import Socket.IO client

const Game = () => {
  const intervalRef = useRef(null);
  const socket = useRef(null); // Reference to the Socket.IO socket

  useEffect(() => {
    // Initialize Socket.IO connection
    socket.current = io("http://localhost:3001"); // Replace with your Socket.IO server URL

    // Listen for messages from the server
    socket.current.on("update", (data) => {
      console.log("Received update:", data);
      // Here you would update your component's state based on the received data
    });

    // Emit an event to the server whenever a button is clicked
    socket.current.on("buttonClick", (id) => {
      console.log(`Button ${id} was pressed`);
      // Send the button click event to the server
      socket.current.emit("buttonClick", id);
    });

    // Fetch updates from the server here
    intervalRef.current = setInterval(() => {
      console.log('Fetching updates...');
      // Example: socket.current.emit("requestUpdate");
    }, 5000); // Call every 5 seconds

    return () => {
      clearInterval(intervalRef.current);
      socket.current.disconnect(); // Clean up on unmount
    };
  }, []);

  const handleButtonClick = (id) => {
    console.log(`Button ${id} was pressed`);
    // Handle button press logic here
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'row' }}>
      {/* Logo Column */}
      <div style={{ width: '20%', backgroundColor: '#f0f0f0', padding: '10px' }}>
        <img src="https://via.placeholder.com/150" alt="Logo" />
      </div>

      {/* Chess Board Column */}
      <div style={{ width: '60%', backgroundColor: '#e0e0e0', padding: '10px' }}>
        <Chessboard width="600px" height="600px" updateData={0/* Pass the updated data here */} />
      </div>

      {/* Right Column */}
      <div style={{ width: '20%', backgroundColor: '#d0d0d0', padding: '10px' }}>
        <button onClick={() => handleButtonClick(1)}>Button 1</button>
        <button onClick={() => handleButtonClick(2)}>Button 2</button>
        <button onClick={() => handleButtonClick(3)}>Button 3</button>
        <button onClick={() => handleButtonClick(4)}>Button 4</button>
        <button onClick={() => handleButtonClick(5)}>Button 5</button>
      </div>
    </div>
  );
};

export default Game;