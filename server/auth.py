# https://www.youtube.com/watch?v=0A_GCXBCNUQ

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
import os
import base64

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION = os.getenv("REMEMBER_ME_EXPIRATION_DAYS")

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
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

###############
## FUNCTIONS ##
###############

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

###############
##  ROUTES   ##
###############
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
    # or not create_user_request.photo  
    if not create_user_request.username or not create_user_request.first_name or not create_user_request.last_name or not create_user_request.email or not create_user_request.phone_number or not create_user_request.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill out all fields.")
    
    # # Validate photo
    # if create_user_request.photo and not is_valid_photo(create_user_request.photo):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Photo must be a valid image.")
    
    
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
async def login_for_access_token(
    request: LoginRequest,
    db: db_dependency
) -> Token:
    
    user = authenticate_user(request.username, request.password, db)
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
    
    access_token_expires = None
    if request.rememberMe:
        access_token_expires = timedelta(days=int(TOKEN_EXPIRATION))
    access_token = create_access_token(user.username, user.user_id, user.user_type, access_token_expires)

    return Token(access_token=access_token, token_type='bearer')
    
@router.get('/users/me', response_model=UserData)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user

# @router.get('/users/me/items')
# async def read_own_items(current_user: dict = Depends(get_current_user)):
#     return [{'item_id': 'Foo', 'owner': current_user.username}]