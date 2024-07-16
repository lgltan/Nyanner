import React from 'react';
import ChessGame from './ChessGame';
import './game.css'

function Game() {
    return (
        <div className="game">
            <div className="game-left-col">
              Nyanner
            </div>
            <div className="chessboard-container">
              <ChessGame />
            </div>
        </div>
    );
}

export default Game;