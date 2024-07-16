from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import date

class PhotoData(BaseModel):
    id: int
    filename: str
    content: str

class CreateUserRequest(BaseModel):
    user_type: int
    username: str
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: datetime

class LoginRequest(BaseModel):
    username: str
    password: str
    rememberMe: bool

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str = None
    user_id: int = None
    user_type: int = None

class UserData(BaseModel):
    user_id: int
    user_type: bool = False
    first_name: str
    last_name: str
    username: str
    email: str
    birthday: date
    phone_number: str
    photo_id: int
    photo: PhotoData
    # password: bytes

class CreateLobbyRequest(BaseModel):
    lobby_name: str
    p1_id: str
    
class JoinLobbyRequest(BaseModel):
    lobby_id: str
    player_id: str

class AdminLogSchema(BaseModel):
    admin_log_id: int
    description: str
    timestamp: datetime
