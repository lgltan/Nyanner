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
from sqlalchemy import or_
from server.schemas import SendMove
import chess
import base64

load_dotenv()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/game',
    tags=['game']
)

# get chessboard (inputs: current user, auth check) returns latest move from db query
# which game the current user is playing
def get_prev_board(db: db_dependency, current_user: User = Depends(get_current_user)):
    user_id = current_user.user_id
    # # get the user's current lobby id
    lobby = db.query(Lobby).filter(or_(Lobby.lobby_status == "Ongoing", Lobby.p1_id == user_id)).first()
    if not lobby:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to find lobby."})

    # # using current lobby id, query from moves table
    move = db.query(Move).filter(Move.lobby_id == lobby.lobby_id).first()
    if not move:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to find lobby."})


# gets called and passes requested move board
@router.post('/val_move', status_code=status.HTTP_200_OK)
async def validate_move(
    request: SendMove,
    db: db_dependency, 
    current_user: User = Depends(get_current_user),
    ):
    
    previous_board = get_prev_board(db_dependency, current_user)


    print(current_user.first_name)
    print(request.fen)


    return True

#      lobby.p2_id = current_user.user_id
#       lobby.lobby_status = EnumStatus['ongoing']
