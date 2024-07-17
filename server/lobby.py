from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import Lobby
from dotenv import load_dotenv
from server.schemas import EnumStatus
from server.utils import db_dependency
import base64
from server.models import AdminLog, User, Session as UserSession
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

    user_id = current_user.user_id
    access_code = generate_unique_id()
    
    if not access_code or not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to create lobby."})

    new_lobby = Lobby(
        lobby_code=access_code.encode('ascii'),
        p1_id=user_id,
        lobby_status=EnumStatus['waiting']
    )
    
    db.add(new_lobby)
    db.commit()
    return access_code
    
@router.put('/join/{access_code}', status_code=status.HTTP_201_CREATED)
async def join_lobby(
    db: db_dependency, 
    access_code: str, 
    current_user: User = Depends(get_current_user)
    ):

    lobby = db.query(Lobby).filter(Lobby.lobby_code == access_code).first()
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Bad request."})

    if not lobby:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Invalid access code."})

    lobby.lobby_code = access_code.encode('ascii')
    lobby.p2_id = current_user.user_id
    lobby.lobby_status = EnumStatus['ongoing']

    db.commit()
    db.refresh(lobby)
    
@router.post('/create/bots', status_code=status.HTTP_201_CREATED)
async def create_bots(
    db: db_dependency, 
    current_user: User = Depends(get_current_user)
    ):

    user_id = current_user.user_id
    access_code = generate_unique_id()
    
    if not access_code or not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to create lobby."})

    new_lobby = Lobby(
        lobby_code=access_code.encode('ascii'),
        p1_id=user_id,
        p2_id=0,
        lobby_status=EnumStatus['ongoing']
    )
    
    db.add(new_lobby)
    db.commit()
    return
    
@router.get('/info', status_code=status.HTTP_201_CREATED)
async def get_lobby(
    db: db_dependency, 
    current_user: User = Depends(get_current_user)
    ):

    user_id = current_user.user_id
    lobby = db.query(Lobby).filter(Lobby.p1_id == user_id and Lobby.p2_id == user_id).first()
    
    print(lobby)
    
    if not lobby:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to find lobby."})
    else:
        return lobby