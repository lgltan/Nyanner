# https://www.youtube.com/watch?v=0A_GCXBCNUQ

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
import base64

load_dotenv()

router = APIRouter(
    prefix='/lobby',
    tags=['lobby']
)

###############
##  ROUTES   ##
###############


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_lobby(db: db_dependency, 
                        lobby_name: str = Form(...),
                        p1_id: str = Form(...),
    ):

    create_lobby_request = CreateLobbyRequest(
        lobby_name="",
        p1_id="",
        
    )
    
    if not create_lobby_request.lobby_name or not create_lobby_request.p1_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Please fill out all fields."})

#     new_lobby = Lobby(
#         lobby_name=create_lobby_request.lobby_name.encode('ascii'),
#         p1_id=create_lobby_request.p1_id.encode('ascii'),
#     )
    
#     db.add(new_lobby)
#     db.commit()
    
@router.put('/join', status_code=status.HTTP_201_CREATED)
async def join_lobby(db: db_dependency, 
                        lobby_id: str = Form(...),
                        player_id: str = Form(...),
    ):

    join_lobby_request = JoinLobbyRequest(
        lobby_id="",
        player_id="",
    )
    
    if not join_lobby_request.lobby_id or not join_lobby_request.player_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Please fill out all fields."})

#     join_lobby = Lobby(
#         lobby_id=join_lobby_request.lobby_id.encode('ascii'),
#         player_id=join_lobby_request.player_id.encode('ascii'),
#     )
    
#     db.add(join_lobby)
#     db.commit()
