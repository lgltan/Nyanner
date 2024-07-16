// p1 always == createLobby host or playBots
// p2 is either the player or the bot
// receive player color - compare player id with currently logged in to player 1 or player 2 in game state
// insert game logic which sends the board state representation as a string as soon as the piece is dropped, wait for response from server to see if it is a valid move
import React, { useState } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';

const ChessGame = () => {
    const [fen, setFen] = useState('start');
    const [game, setGame] = useState(new Chess());

    const onDrop = ({ sourceSquare, targetSquare }) => {
        // Determine if the move involves a pawn promotion
        const isPawnPromotion = /p/.test(sourceSquare[0]);
    
        // Attempt to make the move
        let moveResult = null;
        if (isPawnPromotion) {
            const promotion = window.prompt("Promote to what piece? (e.g., q for queen, r for rook, b for bishop, n for knight):") || 'q'; // Default to queen if no input
            moveResult = game.move({
                from: sourceSquare,
                to: targetSquare,
                promotion: promotion,
            });
        } else {
            moveResult = game.move({ from: sourceSquare, to: targetSquare });
        }
    
        // Check if the move was successful
        if (!moveResult) {
            alert("Invalid move");
        } else {
            setFen(game.fen());
            if (game.game_over()) {
                alert(`Game over! ${game.status()}`);
            }
        }
    };

    return <Chessboard position={fen} onDrop={onDrop} />;
};

export default ChessGame;
