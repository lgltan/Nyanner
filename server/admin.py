from datetime import datetime, timedelta
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from server.database import SessionLocal
from server.models import AdminLog, User, BannedUsers
from server.schemas import UserlistAdmin, BanRequest, UnbanRequest
from server.utils import db_dependency, handle_error
from server.log_utils import log_message
from starlette import status

log_file = "app.log"

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.get('/users', response_model=List[UserlistAdmin])
async def get_all_users(db: db_dependency):
    try:
        users = db.query(User).all()
        return users
    except Exception as exc:
        handle_error(exc, message="Failed to get all users")

@router.get('/logs', response_model=List[dict])
async def get_all_logs(db: db_dependency):
    try:
        logs = db.query(AdminLog).all()
        return [{"admin_log_id": log.admin_log_id, "admin_description": log.admin_description, "admin_timestamp": log.admin_timestamp} for log in logs]
    except Exception as exc:
        handle_error(exc, message="Failed to get all logs")

@router.post('/ban', status_code=status.HTTP_202_ACCEPTED)
async def ban_user(ban_request: BanRequest, db: db_dependency):
    try:
        user = db.query(User).filter(User.user_id == ban_request.user_id).first()
        if not user:
            raise ValueError("User not found")

        # If user is admin don't ban
        if user.user_type:
            raise ValueError("Cannot ban an admin user")

        # Writing to the banned user table
        banned_user = db.query(BannedUsers).filter(BannedUsers.key_to_user_id == user.user_id).first()
        if not banned_user:
            banned_user = BannedUsers(key_to_user_id=user.user_id, ban_bool=True, ban_time=ban_request.ban_duration)
            db.add(banned_user)
        else:
            banned_user.ban_bool = True
            banned_user.ban_timestamp = datetime.now()
            banned_user.ban_time = ban_request.ban_duration

        db.commit()

        log_message(db, f"User {user.username} has been banned for {ban_request.ban_duration} minutes.")
   
        return {"message": "User banned successfully"}
    except Exception as exc:
        handle_error(exc, message="Failed to ban user")

@router.post('/unban', status_code=status.HTTP_204_NO_CONTENT)
async def unban_user(unban_request: UnbanRequest, db: db_dependency):
    try:
        user = db.query(User).filter(User.user_id == unban_request.user_id).first()
        if not user:
            raise ValueError("User not found")

        banned_user = db.query(BannedUsers).filter(BannedUsers.key_to_user_id == user.user_id).first()
        if banned_user:
            banned_user.ban_bool = False
            banned_user.ban_timestamp = None
            banned_user.ban_time = 0
            db.commit()

        log_message(db, f"User {user.username} has been unbanned.")
   
        return {"message": "User unbanned successfully"}
    except Exception as exc:
        handle_error(exc, message="Failed to unban user")
