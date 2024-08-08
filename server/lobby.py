from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette import status
from server.database import SessionLocal
from server.models import Lobby, Move
from dotenv import load_dotenv
from server.schemas import EnumStatus, BotDifficulty
from server.utils import db_dependency, handle_error
import base64
from server.models import AdminLog, User, BannedUsers 
from server.game_utils import get_current_user, generate_unique_id

load_dotenv()

router = APIRouter(
    prefix='/lobby',
    tags=['lobby']
)

###############
##  ROUTES   ##
###############

# NOTE: get_current_user checks if session token is valid built into it

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_lobby(
    db: db_dependency, 
    current_user: User = Depends(get_current_user)
):
    try:
        user_id = current_user.user_id

        waiting_game = db.query(Lobby).filter(Lobby.lobby_status == "Waiting").filter(Lobby.p1_id == user_id).first()
        if waiting_game:
            db.delete(waiting_game)
            db.commit()
        ongoing_game = db.query(Lobby).filter(Lobby.lobby_status == "Ongoing").filter(or_(Lobby.p1_id == user_id, Lobby.p2_id == user_id)).first()
        if ongoing_game:
            return # should redirect player to the game they are currently in automatically

        access_code = generate_unique_id()

        if not access_code or not user_id:
            raise ValueError("Failed to create lobby.")

        new_lobby = Lobby(
            lobby_code=access_code.encode('ascii'),
            p1_id=user_id,
            lobby_status=EnumStatus['waiting'],
            bot_diff=0
        )

        db.add(new_lobby)
        db.commit()
        return access_code
    except Exception as exc:
        handle_error(exc, message="Failed to create lobby")

@router.put('/join/{access_code}', status_code=status.HTTP_201_CREATED)
async def join_lobby(
    db: db_dependency, 
    access_code: str, 
    current_user: User = Depends(get_current_user)
):
    try:
        lobby = db.query(Lobby).filter(Lobby.lobby_code == access_code).first()

        if not current_user:
            raise ValueError("Bad request.")

        if not lobby:
            raise ValueError("Invalid access code.")

        lobby.lobby_code = access_code.encode('ascii')

        if current_user.user_id == lobby.p1_id or current_user.user_id == lobby.p2_id:
            pass
        else:
            lobby.p2_id = current_user.user_id
            lobby.lobby_status = EnumStatus['ongoing']

            db.commit()
            db.refresh(lobby)

            zero_move = Move(
                lobby_id=lobby.lobby_id,
                board='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
            )

            db.add(zero_move)
            db.commit()
    except Exception as exc:
        handle_error(exc, message="Failed to join lobby")

@router.post('/create/bots', status_code=status.HTTP_201_CREATED)
async def create_bots(
    request: BotDifficulty,
    db: db_dependency, 
    current_user: User = Depends(get_current_user),
):
    try:
        user_id = current_user.user_id
        access_code = generate_unique_id()

        if not access_code or not user_id:
            raise ValueError("Failed to create lobby.")

        new_lobby = Lobby(
            lobby_code=access_code.encode('ascii'),
            p1_id=user_id,
            p2_id=0,
            lobby_status=EnumStatus['ongoing'],
            bot_diff=request.diffLvl
        )

        db.add(new_lobby)
        db.commit()
    except Exception as exc:
        handle_error(exc, message="Failed to create lobby with bots")

@router.get('/info', status_code=status.HTTP_201_CREATED)
async def get_lobby(
    db: db_dependency, 
    current_user: User = Depends(get_current_user)
):
    try:
        user_id = current_user.user_id

        lobby = db.query(Lobby).filter(or_(Lobby.lobby_status == "Waiting", Lobby.lobby_status == "Ongoing")).filter(or_(Lobby.p1_id == user_id, Lobby.p2_id == user_id)).first()

        if lobby:
            p1_id = db.query(Lobby).filter(Lobby.lobby_code == lobby.lobby_code).first().p1_id
            p2_id = db.query(Lobby).filter(Lobby.lobby_code == lobby.lobby_code).first().p2_id
        else:
            raise ValueError("Failed to find lobby.")

        if p1_id:
            lobby.p1_name = db.query(User).filter(User.user_id == p1_id).first().username
        if p2_id:
            lobby.p2_name = db.query(User).filter(User.user_id == p2_id).first().username

        if not lobby:
            raise ValueError("Failed to find lobby.")
        else:
            return lobby
    except Exception as exc:
        handle_error(exc, message="Failed to get lobby info")

@router.get('/current_player', status_code=status.HTTP_201_CREATED)
async def get_current_player(
    db: db_dependency, 
    current_user: User = Depends(get_current_user)
):
    try:
        user_id = current_user.user_id
        lobby = db.query(Lobby).filter(or_(Lobby.lobby_status == "Waiting", Lobby.lobby_status == "Ongoing")).filter(or_(Lobby.p1_id == user_id, Lobby.p2_id == user_id)).first()

        if lobby:
            p1_id = lobby.p1_id
            p2_id = lobby.p2_id
        if p1_id:
            if user_id == p1_id:
                return "white"
        if p2_id:
            if user_id == p2_id:
                return "black"
    except Exception as exc:
        handle_error(exc, message="Failed to get current player")

@router.get('/ingame_check', status_code=status.HTTP_201_CREATED)
async def get_ingame_check(
    db: db_dependency, 
    current_user: User = Depends(get_current_user)
):
    try:
        game = db.query(Lobby).filter(or_(Lobby.lobby_status == "Waiting", Lobby.lobby_status == "Ongoing")).filter(or_(Lobby.p1_id == current_user.user_id, Lobby.p2_id == current_user.user_id)).first()

        if game:
            return True
        else:
            return False
    except Exception as exc:
        handle_error(exc, message="Failed to check in-game status")

@router.put('/leave_game/{access_code}', status_code=status.HTTP_201_CREATED)
async def leave_game(
    db: db_dependency, 
    access_code: str, 
    current_user: User = Depends(get_current_user)
):
    try:
        lobby = db.query(Lobby).filter(Lobby.lobby_code == access_code).first()

        if not current_user:
            raise ValueError("Bad request.")

        if not lobby:
            raise ValueError("Invalid access code.")

        if current_user.user_id == lobby.p1_id or current_user.user_id == lobby.p2_id:
            lobby.lobby_status = EnumStatus['archived']
            db.commit()
            db.refresh(lobby)
            return True
        else:
            return False
    except Exception as exc:
        handle_error(exc, message="Failed to leave game")
