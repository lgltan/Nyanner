import React, { useState } from 'react';

const Chessboard = () => {
  const [pieces, setPieces] = useState(Array(64).fill(null)); // Initialize with nulls
  const [dragging, setDragging] = useState(null);

  const handleDragStart = (index) => {
    setDragging(index);
  };

  setPieces([
    ...pieces.slice(0, 1), // Keep the existing state
    { type: 'pawn', color: 'black' }, // Add a pawn at position 1 (0-indexed)
    ...pieces.slice(2), // Continue with the rest of the state
  ]);
  

  const handleDragEnd = () => {
    setDragging(null); // Reset after drop
  };

  const handleDrop = (index) => {
    if (!dragging || index === dragging) return; // Prevent self-drop

    // Swap pieces
    const newPieces = [...pieces];
    [newPieces[dragging], newPieces[index]] = [null, pieces[dragging]];
    setPieces(newPieces);
    setDragging(null); // Reset after successful drop
  };

  return (
    <div className="chess-board">
      {[...Array(8)].map((_, i) =>
        <div className="row" key={i}>
          {[...Array(8)].map((_, j) =>
            <Square
              key={j}
              index={`${i}-${j}`}
              piece={pieces[j + i * 8]}
              onDragStart={() => handleDragStart(j + i * 8)}
              onDragEnd={handleDragEnd}
              onDrop={(e) => {
                e.preventDefault();
                handleDrop(j + i * 8);
              }}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default Chessboard;
