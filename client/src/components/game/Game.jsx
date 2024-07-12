// p1 always == createLobby host or playBots
// p2 is either the player or the bot
// receive player color - compare player id with currently logged in to player 1 or player 2 in game state
// insert game logic which sends the board state representation as a string as soon as the piece is dropped, wait for response from server to see if it is a valid move
import React, { useState } from 'react';
import axios from 'axios';

const Game = ({ props }) => {
    const { lobbyId } = props.lobbyId || 0; // Extract the lobby ID from the URL

    const squaresArray = Array(64).fill().map((_, index) => ({
        id: index.toString(),
        color: (index & 7) === 0 || (index & 7) === 7 || (index & 56) === 0 || (index & 56) === 63 ? 'white' : 'black',
    }));

    const [draggedPiece, setDraggedPiece] = useState(null);
    const [targetSquare, setTargetSquare] = useState(null);
    const [squares, setSquares] = useState(squaresArray);
    const [pieces, setPieces] = useState({});

    const updateBoardState = (newBoardState) => {
        setSquares(newBoardState);
    };

    const handleDragStart = (piece) => {
        setDraggedPiece(piece);
    };

    const handleDragOver = (square) => {
        setTargetSquare(square);
    };

    const handleDrop = async (square) => {
        if (!draggedPiece) return;

        // Perform the move logic here
        // For simplicity, this example doesn't include move validation
        const newBoardState = [...squares]; // Copy the board state
        const pieceIndex = newBoardState.findIndex(p => p.id === draggedPiece.position);
        newBoardState[pieceIndex].id = square.id;
        newBoardState[square.id].id = draggedPiece.position;

        // Update the board state
        setSquares(newBoardState);

        // Reset dragged piece and target square
        setDraggedPiece(null);
        setTargetSquare(null);

        // Call the API to validate the move
        try {
            const response = await axios.post(`YOUR_API_ENDPOINT_TO_VALIDATE_MOVE`, {
                sourceSquare: draggedPiece.position,
                targetSquare,
            });

            // Handle the API response here
            // For example, revert the move if it's invalid
            if (!response.data.isValidMove) {
                const revertBoardState = [...squares]; // Revert the board state
                const pieceIndex = revertBoardState.findIndex(p => p.id === square.id);
                revertBoardState[pieceIndex].id = draggedPiece.position;
                revertBoardState[draggedPiece.position].id = square.id;
                setSquares(revertBoardState);
            }
        } catch (error) {
            console.error("Failed to validate move", error);
        }
    };


    return (
        <div>
            <h1>Game Page</h1>
            <p>Lobby ID: {lobbyId}</p>

            <div className="chessboard">
                {squares.map((square) => (
                    <div
                        key={square.id}
                        className={`square ${square.color}`}
                        draggable
                        onDragStart={() => handleDragStart(square.id)}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => handleDrop(e, square.id)}
                    >
                        {pieces[square.color].find((piece) => piece.position === square.id)?.type}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Game;