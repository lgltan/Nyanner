from datetime import datetime, timedelta
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.database import SessionLocal
from server.models import AdminLog, User, BannedUsers
from server.schemas import UserlistAdmin, BanRequest, UnbanRequest
from server.auth import db_dependency
from starlette import status
import logging

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


@router.post('/ban', status_code=status.HTTP_202_ACCEPTED)
async def ban_user(ban_request: BanRequest, db: db_dependency):
    logging.info(f"Received ban request: {ban_request}")

    user = db.query(User).filter(User.user_id == ban_request.user_id).first()
    if not user:
        logging.error(f"User with ID {ban_request.user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")

    banned_user = db.query(BannedUsers).filter(BannedUsers.key_to_user_id == user.user_id).first()
    if not banned_user:
        logging.info("Creating new session")
        banned_user = BannedUsers(key_to_user_id=user.user_id, ban_bool=True, ban_time=ban_request.ban_duration)
        db.add(banned_user)
    else:
        logging.info("Banned Session exists, updating")
        banned_user.ban_bool = True
        banned_user.ban_timestamp = datetime.now()
        banned_user.ban_time = ban_request.ban_duration

    db.commit()

    new_log = AdminLog(
        admin_description=f"User {user.username} has been banned for {ban_request.ban_duration} minutes.",
        admin_timestamp=datetime.now()
    )
    db.add(new_log)
    db.commit()

    logging.info(f"User {user.username} banned successfully.")
    return {"message": "User banned successfully"}


@router.post('/unban', status_code=204)
async def unban_user(unban_request: UnbanRequest, db: db_dependency):
    user = db.query(User).filter(User.user_id == unban_request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    banned_user = db.query(BannedUsers).filter(BannedUsers.key_to_user_id == user.user_id).first()
    if banned_user:
        banned_user.ban_bool = False
        banned_user.ban_timestamp = None
        banned_user.ban_time = 0
        db.commit()

    new_log = AdminLog(
        admin_description=f"User {user.username} has been unbanned.",
        admin_timestamp=datetime.now()
    )
    db.add(new_log)
    db.commit()

    return {"message": "User unbanned successfully"}
