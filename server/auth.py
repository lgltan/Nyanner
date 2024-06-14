# https://www.youtube.com/watch?v=0A_GCXBCNUQ

from datetime import timedelta, datetime
from typing import Annotated, Optional
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
import os
from PIL import Image

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

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
    photo: Photo
    
    @field_validator('photo')
    def validate_photo():
        try:
            with Image.open(photo) as img:
                img.verify()
                return True
        except (IOError, SyntaxError):
            return False
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
    # or not create_user_request.photo  
    if not create_user_request.username or not create_user_request.first_name or not create_user_request.last_name or not create_user_request.email or not create_user_request.phone_number or not create_user_request.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill out all fields.")
    
    # implement regex for input validation here
    
    create_user_model = User(
        user_type=0,
        username=create_user_request.username.encode('ascii'),
        first_name=create_user_request.first_name.encode('ascii'),
        last_name=create_user_request.last_name.encode('ascii'),
        email=create_user_request.email.encode('ascii'),
        phone_number=create_user_request.phone_number.encode('ascii'),
        # photo=create_user_request.photo,
        password=bcrypt_context.hash(create_user_request.password).encode('ascii'),
    )
    
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
    token = create_access_token(user.username, user.user_id, timedelta(minutes=5))
    
    return {'access_token': token, 'token_type': 'bearer'}
    
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        user_id: int = payload.get('user_id')
        user_type: int = payload.get('user_type')
        first_name: str = payload.get('first_name')
        last_name: str = payload.get('last_name')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
        return {'username': username, 'id': user_id, 'user_type': user_type, 'first_name': first_name, 'last_name': last_name}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
@router.post("/logout", response_status=status.HTTP_200_OK)
async def logout(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    # Verify the refresh token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid')

    invalidate_token(token, db)
    return {"detail": "Logged out successfully"}


def invalidate_token(token: str, db: Session):
    issued_token = db.query(IssuedToken).filter(IssuedToken.id == token).first()
    if issued_token:
        issued_token.invalidated = True
        db.commit()