from datetime import timedelta, datetime
from typing import Annotated, Optional, Union
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, HttpUrl, field_validator
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import User, IssuedToken
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from server.schemas import Photo, CreateUserRequest, LoginRequest, Token, TokenData, UserData
import os
import base64

load_dotenv()

# router = APIRouter(
#     prefix='/auth',
#     tags=['auth']
# )

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION = os.getenv("REMEMBER_ME_EXPIRATION_DAYS")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# Function to verify if the photo is a valid image
def is_valid_photo(photo: str) -> bool:
    try:
        _, ext = os.path.splitext(photo)
        if ext.lower() not in ['.jpg', '.jpeg', '.png']:
            return False
        # Decode the Base64 string to get the raw bytes
        decoded_data = base64.b64decode(photo)
        
        # Check the first few bytes to see if they match known image file signatures
        jpeg_signature = b'\xFF\xD8\xff'
        png_signature = b'\x89PNG\r\n\x1a\n'
        
        # Check for JPEG signature
        if decoded_data[:3] == jpeg_signature:
            return True
        # Check for PNG signature
        elif decoded_data[:8] == png_signature:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: int, user_type: int, expires_delta: Union[timedelta, None]):
    encode = {'username': username, 'id': user_id, 'user_type': user_type}
    expires = datetime.utcnow() + timedelta(minutes=30)
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        user_id: int = payload.get('id')
        user_type: int = payload.get('user_type')
        if username is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id, user_type=user_type)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
