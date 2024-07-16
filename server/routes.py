# https://www.youtube.com/watch?v=0A_GCXBCNUQ

from datetime import timedelta
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import AdminLog, User, Photo
from passlib.context import CryptContext
from dotenv import load_dotenv
from server.schemas import CreateUserRequest, LoginRequest, Token, TokenData, UserData
from server.auth import validate_image, validate_user_data, authenticate_user, create_access_token, get_current_active_user, db_dependency, bcrypt_context, TOKEN_EXPIRATION
import os

load_dotenv()

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

###############
##  ROUTES   ##
###############

@router.get('/users', response_model=List[UserData])
async def get_all_users(db: db_dependency):
    users = db.query(User).all()
    return users

@router.get('/logs', response_model=List[dict])
async def get_all_logs(db: db_dependency):
    logs = db.query(AdminLog).all()
    return [{"log_id": log.admin_log_id, "description": log.description, "timestamp": log.timestamp} for log in logs]

