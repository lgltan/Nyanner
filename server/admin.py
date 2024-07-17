from datetime import datetime, timedelta
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.database import SessionLocal
from server.models import AdminLog, User, Session
from server.schemas import UserlistAdmin
from server.auth import db_dependency

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

@router.post('/ban/{user_id}', status_code=200)
async def ban_user(user_id: int, ban_duration: int, db: db_dependency):
    user_session = db.query(Session).filter(Session.user_id == user_id).first()
    if not user_session:
        user_session = Session(user_id=user_id, ban_bool=True, ban_time=ban_duration)
        db.add(user_session)
    else:
        user_session.ban_bool = True
        user_session.ban_time = ban_duration
        user_session.ban_timestamp = datetime.now()
    db.commit()
    return {"message": "User banned successfully"}

@router.post('/unban/{user_id}', status_code=200)
async def unban_user(user_id: int, db: db_dependency):
    user_session = db.query(Session).filter(Session.user_id == user_id).first()
    if not user_session:
        raise HTTPException(status_code=404, detail="User session not found")
    user_session.ban_bool = False
    db.commit()
    return {"message": "User unbanned successfully"}
