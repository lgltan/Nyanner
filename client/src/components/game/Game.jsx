// page for the game proper

// main loop
// - check db for game state - current board, current phase
// - - possible actions: [move unit, purchase unit, roll for new units, purchase xp]
// - submit action log to backend

// backend
// - figure out a way to sync actual chessboard and timings

import React, { useEffect, useRef } from 'react';
import ChessBoard from './ChessBoard';

const GameScreen = () => {
  const intervalRef = useRef(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      // Fetch updates from the server here
      console.log('Fetching updates...');
      // Example: fetchDataFromServer().then(data => setBoardData(data));
    }, 5000); // Call every 5 seconds

    return () => clearInterval(intervalRef.current);
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
        <ChessBoard width="600px" height="600px" updateData={0/* Pass the updated data here */} />
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

export default GameScreen;
