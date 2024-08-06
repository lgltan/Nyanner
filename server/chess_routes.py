from datetime import timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
# from server.models import Lobby
from dotenv import load_dotenv
from server.schemas import CreateLobbyRequest, JoinLobbyRequest
from server.utils import db_dependency
from server.game_utils import get_current_user, get_new_move
from server.models import User, Lobby, Move
from sqlalchemy import or_
import base64

load_dotenv()

router = APIRouter(
    prefix='/game',
    tags=['game']
)

# get chessboard (inputs: current user, auth check) returns latest move from db query
# which game the current user is playing
def get_prev_board(db: db_dependency, current_user: User = Depends(get_current_user)):
    user_id = current_user.user_id

    # get the user's current lobby id
    lobby = db.query(Lobby).filter(Lobby.lobby_status == "Ongoing", Lobby.p1_id == user_id).first()
    if not lobby:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to find lobby."})

    # using current lobby id, query from moves table
    move = db.query(Move).filter(Move.lobby_id == lobby.value).first()
    if not move:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to find lobby."})

    return move.board

# use sunfish, 2 string inputs; board states, get previous board state, given new board state, check difference with sunfish
# post board to db if valid
# return boolean true or false
# post move (inputs: new chessboard string, auth check) returns true if move is valid, false if invalid
# needs to do move validation, to be added after 

# gets called and passes requested move board
@router.post('/validate_board', status_code=status.HTTP_200_OK)
async def validate_board(
    db: db_dependency, 
    current_user: User = Depends(get_current_user),
    new_board: Move = Depends(get_new_move), # obtain requested move board
    ):
    
    prevboard = get_prev_board(db, current_user) # get previous board and save here

    # compare previous board with requested move board

    # if true
    new_move = Move(
        
    )
    
    db.add(new_move)
    db.commit()
    return True

    # if False
    return False

