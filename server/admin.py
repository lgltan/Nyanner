from datetime import timedelta
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import AdminLog, User, Photo
from server.schemas import UserlistAdmin
from server.auth import db_dependency, TOKEN_EXPIRATION

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.get('/users', response_model=List[UserlistAdmin])
async def get_all_users(db: db_dependency):
    users = db.query(User).all()
    return users

@router.get('/logs', response_model=List[dict])
async def get_all_logs(db: db_dependency):
    logs = db.query(AdminLog).all()
    return [{"admin_log_id": log.admin_log_id, "admin_description": log.admin_description, "admin_timestamp": log.admin_timestamp} for log in logs]
