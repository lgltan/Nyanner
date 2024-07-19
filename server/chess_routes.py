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
    prefix='/game',
    tags=['game']
)

# @ETHAN get chessboard (inputs: current user, auth check) returns latest move from db query
# which game the current user is playing

# @ETHAN post move (inputs: new chessboard string, auth check) returns true if move is valid, false if invalid
# needs to do move validation, to be added after 