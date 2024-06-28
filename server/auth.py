from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from server.schemas import Photo, CreateUserRequest, LoginRequest, Token, TokenData, UserData
import os
import base64
import re

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

def validate_password(password: str):
    password_length = len(password)
    has_lowercase = re.search(r'[a-z]', password) is not None
    has_uppercase = re.search(r'[A-Z]', password) is not None
    has_number = re.search(r'[0-9]', password) is not None
    has_special_character = re.search(r'[!@#$%^&*()_,.?":{}|<>\\-]', password) is not None

    if password_length < 12 or password_length > 32:
        return 'Password must be between 12 and 32 characters long.'
    elif not has_lowercase:
        return 'Password must contain at least one lowercase letter.'
    elif not has_uppercase:
        return 'Password must contain at least one uppercase letter.'
    elif not has_number:
        return 'Password must contain at least one number.'
    elif not has_special_character:
        return 'Password must contain at least one special character.'

    return None

def validate_user_data(user_data: CreateUserRequest, db: db_dependency):
    errors = {}
    # Validate first name
    NAME_REGEX = r'^[a-zA-Z ]{1,50}$'
    if not re.match(NAME_REGEX, user_data.first_name):
        errors['firstName'] = 'First name should only contain letters and spaces.'

    # Validate last name
    if not re.match(NAME_REGEX, user_data.last_name):
        errors['lastName'] = 'Last name should only contain letters and spaces.'

    # Validate username
    USERNAME_REGEX = r'^[a-zA-Z0-9](\w|_){3,15}$'
    if not re.match(USERNAME_REGEX, user_data.username):
        errors['username'] = 'Username should only contain alphanumeric or underscore characters and must be 4-16 characters long.'
    # Check if username already exists
    user = db.query(User).filter(User.username == user_data.username).first()
    if user:
        errors['username'] = 'Username already exists.'
    
    # Validate email
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(EMAIL_REGEX, user_data.email):
        errors['email'] = 'E-mail should not exceed 50 characters'

    # Validate phone number
    PHONE_REGEX = r'^(09|\+639)\d{9}$'
    if not re.match(PHONE_REGEX, user_data.phone_number):
        errors['phoneNumber'] = 'Please enter a valid Philippine phone number'

    # Validate password
    password_error = validate_password(user_data.password)
    if password_error:
        errors['password'] = password_error

    # Validate confirm password
    if user_data.password != user_data.confirm_password:
        errors['confirmPassword'] = 'Passwords do not match.'

    # # Validate photo
    # if create_user_request.photo and not is_valid_photo(create_user_request.photo):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Photo must be a valid image.")
    
    return errors

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
    ALPHANUM_UNDERSCORE_REGEX = r'^[a-zA-Z0-9](\w|_)*$'
    if not re.match(ALPHANUM_UNDERSCORE_REGEX, username):
        return False
    # if len(validate_password(password)) > 0:
    #     return False

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
