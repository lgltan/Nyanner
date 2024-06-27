from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class User(BaseModel):
    user_type: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    # photo: str
    password: str

class Photo(BaseModel):
    url: Optional[HttpUrl] = None
    filename: str = Field(...)
class CreateUserRequest(BaseModel):
    user_type: int
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    # photo: str

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
    user_type: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    # photo: str