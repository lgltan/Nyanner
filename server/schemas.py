from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from datetime import date

class EnumStatus(str, Enum):
    waiting = 'Waiting'
    ongoing = 'Ongoing'
    archived = 'Archived'

class PhotoData(BaseModel):
    id: int
    filename: str
    content: str

class CreateUserRequest(BaseModel):
    user_type: bool
    username: str
    user_password: str
    confirm_password: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: datetime

class LoginRequest(BaseModel):
    username: str
    user_password: str
    rememberMe: bool
    recaptchaToken: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str = None
    user_id: int = None
    user_type: int = None

class UserlistAdmin(BaseModel):
    user_id: int
    username: str
    email: str
    user_type: bool

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

class AdminLogSchema(BaseModel):
    admin_log_id: int
    admin_description: str
    admin_timestamp: datetime

class BanRequest(BaseModel):
    user_id: int
    ban_duration: int

class UnbanRequest(BaseModel):
    user_id: int