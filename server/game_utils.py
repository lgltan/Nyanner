from typing import Annotated, Union
from fastapi import Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import User
from jose import jwt, JWTError
from dotenv import load_dotenv
from server.schemas import TokenData
import string
import random
import os
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
import re
import base64
from server.utils import db_dependency, TOKEN_EXPIRATION

load_dotenv()

# router = APIRouter(
#     prefix='/auth',
#     tags=['auth']
# )

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION = os.getenv("REMEMBER_ME_EXPIRATION_DAYS")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
chars = string.ascii_letters + string.digits

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
        if username is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id, user_type=user_type)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    
    return user

def generate_unique_id(length=6):
    return ''.join(random.choice(chars) for _ in range(length))