// p1 always == createLobby host or playBots
// p2 is either the player or the bot
// receive player color - compare player id with currently logged in to player 1 or player 2 in game state
// insert game logic which sends the board state representation as a string as soon as the piece is dropped, wait for response from server to see if it is a valid move
import React, { useState, useMemo } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import api from '../../services/api';
import { fetchToken } from '../../services/authProvider';

import wK from './pieces/wK.png';
import wQ from './pieces/wQ.png';
import wR from './pieces/wR.png';
import wB from './pieces/wB.png';
import wN from './pieces/wN.png';
import wP from './pieces/wP.png';

import bK from './pieces/bK.png';
import bQ from './pieces/bQ.png';
import bR from './pieces/bR.png';
import bB from './pieces/bB.png';
import bN from './pieces/bN.png';
import bP from './pieces/bP.png';

const ChessGame = () => {
    const [fen, setFen] = useState('start');
    const [game, setGame] = useState(new Chess());

    const pieces = ["wP","wN","wB","wR","wQ","wK","bP","bN","bB","bR","bQ","bK"];
    const pieceImgs = [wP,wN,wB,wR,wQ,wK,bP,bN,bB,bR,bQ,bK]

    const customPieces = useMemo(() => {
        const pieceComponents = {};
        pieces.forEach((piece, i) => {
            pieceComponents[piece] = ({ squareWidth }) => (
                <div
                    style={{
                        width: squareWidth,
                        height: squareWidth,
                        backgroundImage: `url(${pieceImgs[i]})`,
                        backgroundSize: "100%",
                        backgroundRepeat: "no-repeat"
                    }}
                />
            );
        });
        return pieceComponents;
    }, []);

    const onPieceDrop = ({ sourceSquare, targetSquare, piece }) => {
     
        console.log('xxxxxx');
        console.log(piece);

        const move = game.move({
            from: sourceSquare,
            to: targetSquare,
            promotion: piece[1].toLowerCase() ?? "q",
        });
        setGame(game.fen());

        // illegal move
        if (move === null) return false;

        // Update the FEN and game state
        setFen(game.fen());
        setGame(new Chess(game.fen())); // Set the game state correctly

         // exit if the game is over
        if (game.game_over() || game.in_draw()) return false;

        return true;  
    };

    return <Chessboard 
    id="chessboard"
    position={fen} 
    onPieceDrop={onPieceDrop} 
    boardOrientation={"black"} 
    customPieces={customPieces}
    customDarkSquareStyle={{backgroundColor: '#405A86'}} 
    customLightSquareStyle={{backgroundColor: '#F7F7F7'}} 
    customBoardStyle={{border: '16px solid rgb(200, 200, 200)', margin: '20px'}}
    />;
};

export default ChessGame;
