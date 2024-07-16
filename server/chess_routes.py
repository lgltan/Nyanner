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

