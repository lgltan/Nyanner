from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import Lobby
from dotenv import load_dotenv
from server.schemas import CreateLobbyRequest, EnumStatus
from server.utils import db_dependency
import base64

from server.game_utils import get_current_user, generate_unique_id

load_dotenv()

router = APIRouter(
    prefix='/lobby',
    tags=['lobby']
)

###############
##  ROUTES   ##
###############

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_lobby(
    db: db_dependency, 
    current_user: User = Depends(get_current_user)
    ):

    user_id = current_user.user_id
    access_code = generate_unique_id()

    create_lobby_request = CreateLobbyRequest(
        lobby_code=access_code,
        p1_id=user_id
    )
    
    if not create_lobby_request.lobby_id or not create_lobby_request.p1_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Failed to create lobby."})

    new_lobby = Lobby(
        lobby_code=create_lobby_request.lobby_code.encode('ascii'),
        p1_id=create_lobby_request.p1_id.encode('ascii'),
        status=EnumStatus['waiting']
    )
    
    db.add(new_lobby)
    db.commit()
    return access_code
    
@router.put('/join', status_code=status.HTTP_201_CREATED)
async def join_lobby(
    db: db_dependency, 
    access_code: str = Form(...), 
    current_user: User = Depends(get_current_user)
    ):

    lobby = db.query(Lobby).filter(Lobby.lobby_code == access_code).first()
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Bad request."})

    if not lobby:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Invalid access code."})

    lobby.lobby_code = lobby_code
    lobby.p2_id = current_user.user_id
    lobby.status = EnumStatus['ongoing']

    db.commit()
    db.refresh(lobby)