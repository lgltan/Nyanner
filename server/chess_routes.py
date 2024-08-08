from datetime import timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
# from server.models import Lobby
from dotenv import load_dotenv
from server.utils import db_dependency
from server.game_utils import get_current_user, get_new_move
from server.game.game import get_uci, check_castling, get_index, check_enpassant, get_movelist, sunfish_to_FEN
from server.models import User, Lobby, Move
from sqlalchemy import or_, and_
from server.schemas import SendMove
import chess
import base64

load_dotenv()

router = APIRouter(
    prefix='/game',
    tags=['game']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get chessboard (inputs: current user, auth check) returns latest move from db query
# which game the current user is playing
def get_prev_board(db: db_dependency, current_user: User = Depends(get_current_user)):
    user_id = current_user.user_id
    
    print('HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
    
    # # get the user's current lobby id
    lobby = db.query(Lobby).filter(
        (and_(Lobby.lobby_status == "Ongoing", or_(Lobby.p1_id == user_id, Lobby.p2_id == user_id) ) )).first()
    if not lobby:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to find lobby."})

    print(lobby.lobby_id)
    # # using current lobby id, query from moves table
    move = db.query(Move).filter(Move.lobby_id == lobby.lobby_id).first()
    if move == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to find lobby."})

    return move.board


# gets called and passes requested move board
@router.post('/val_move', status_code=status.HTTP_200_OK)
async def val_move(
    request: SendMove,
    db: db_dependency, 
    current_user: User = Depends(get_current_user),
    ):
    

    print(current_user.first_name)
    print(request.fen)
    previous_board = get_prev_board(db, current_user)
    
    board = chess.Board(fen=previous_board)
    if not board.is_valid():
        print('error')

    # checks if move is valid
    move = chess.Move.from_uci(request.uci)
    print('WALDOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
    print(board.legal_moves)
    print(move in board.legal_moves)

    return True
