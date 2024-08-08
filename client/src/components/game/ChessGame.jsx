// p1 always == createLobby host or playBots
// p2 is either the player or the bot
// receive player color - compare player id with currently logged in to player 1 or player 2 in game state
// insert game logic which sends the board state representation as a string as soon as the piece is dropped, wait for response from server to see if it is a valid move
import React, { useState, useMemo, useEffect } from 'react';
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

const ChessGame = ({playerColor}) => {
    const game = useMemo(() => new Chess(), []);
    const [isBot, setIsBot] = useState();
    const [gamePosition, setGamePosition] = useState(game.fen());

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

    useEffect(() => {
        const updateBoard = async () => {
            try {
                const token = fetchToken();
                const response = await api.get('/game/get_prev_board', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
              });
              setGamePosition(response.data);
            } catch (error) {  
            }
          };
          updateBoard();
    }, []);

    const onDrop = async (sourceSquare, targetSquare, piece) => {
        const move = game.move({
            from: sourceSquare,
            to: targetSquare,
            promotion: piece[1].toLowerCase() ?? "q",
        });
        // illegal move
        if (move === null) return false;

        // Update the FEN and game state
        setGamePosition(game.fen());

         // exit if the game is over
        if (game.isGameOver() || game.isDraw()) {
            alert("Checkmate.")
            return false;
        }

        try {
            console.log('hi');
            const token = fetchToken();
            const request = {
                'fen': game.fen(),
                'uci': '' + sourceSquare + targetSquare
            };
            const response = api.post('/game/val_move', request, {
                headers: {
                    'Content_Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                }
            });
            console.log(response);
        } catch (error) {
            console.error(error);
        }

        return true;  
    };


    return <Chessboard 
    id="chessboard"
    position={gamePosition} 
    onPieceDrop={onDrop} 
    boardOrientation={playerColor} 
    customPieces={customPieces}
    customDarkSquareStyle={{backgroundColor: '#405A86'}} 
    customLightSquareStyle={{backgroundColor: '#F7F7F7'}} 
    customBoardStyle={{border: '16px solid rgb(200, 200, 200)', margin: '20px'}}
    />;
};

export default ChessGame;
