from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import User, Photo
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from server.schemas import CreateUserRequest, TokenData
import os
import re
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

# Function to verify if the photo is a valid image
def validate_image(file: UploadFile) -> bool:
    magic_numbers = {
        b'\xff\xd8\xff': 'jpeg',
        b'\x89PNG\r\n\x1a\n': 'png',
        b'GIF87a': 'gif',
        b'GIF89a': 'gif',
    }
    
    try:
        content = file.file.read(10)
        file.file.seek(0)
        for magic, filetype in magic_numbers.items():
            if content.startswith(magic):
                return True
    except Exception as e:
        return False
    return False

def validate_name(name: str) -> bool:
    NAME_REGEX = r'^[a-zA-Z ]{1,50}$'
    return re.match(NAME_REGEX, name)

def validate_phone_number(phone_number: str) -> bool:
    PHONE_REGEX = r'^(09|\+639)\d{9}$'
    return re.match(PHONE_REGEX, phone_number)

def validate_birthday(birthday):    
    today = datetime.now()
    max_age = 150
    min_age = 1
    earliest_valid_date = today - timedelta(days=max_age * 365)
    latest_valid_date = today - timedelta(days=min_age * 365)

    if birthday >= today or birthday < earliest_valid_date or birthday > latest_valid_date:
        return False
    else:
        return True

def validate_user_data(db: db_dependency, user_data: CreateUserRequest, file: UploadFile = None):
    errors = {}
    # Validate first name
    if not validate_name(user_data.first_name):
        errors['firstName'] = 'First name should only contain letters and spaces.'

    # Validate last name
    if not validate_name(user_data.last_name):
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
    if not validate_phone_number(user_data.phone_number):
        errors['phoneNumber'] = 'Please enter a valid Philippine phone number'

    # Validate birthday
    if not validate_birthday(user_data.birthday):
        errors['birthday'] = 'Please enter a valid birthday.'
        
    # Validate password
    password_error = validate_password(user_data.user_password)
    if password_error:
        errors['password'] = password_error

    # Validate confirm password
    if user_data.user_password != user_data.confirm_password:
        errors['confirmPassword'] = 'Passwords do not match.'

    # # Validate photo
    if file:
        if not validate_image(file):
            errors['profilePhoto'] = 'Invalid photo file.'
    
    return errors

def authenticate_user(username: str, password: str, db):
    ALPHANUM_UNDERSCORE_REGEX = r'^[a-zA-Z0-9](\w|_)*$'
    if not re.match(ALPHANUM_UNDERSCORE_REGEX, username):
        return False
    # if len(validate_password(password)) > 0:
    #     return False

    user = db.query(User).filter(User.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.user_password):
        return False
    return user

def create_access_token(username: str, user_id: int, user_type: int, expires_delta: Union[timedelta, None]):
    encode = {'username': username, 'id': user_id, 'user_type': user_type}
    expires = datetime.utcnow() + timedelta(minutes=180)    # Default expiration time is 3 hours
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
    
    photo = db.query(Photo).filter(Photo.id == user.photo_id).first()
    if photo is None:
        raise credentials_exception
    
    return { 'user': user, 'photo': photo }

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    # if current_user['user'].disabled:
    #     raise HTTPException(status_code=400, detail='Inactive user')
    current_user['photo'].id = current_user['photo'].id
    current_user['photo'].filename = current_user['photo'].filename
    current_user['photo'].content = base64.b64encode(current_user['photo'].content).decode('ascii')
    return current_user

async def get_photo_from_db(image_id: int, db: db_dependency):
    photo = db.query(Photo).filter(Photo.id == image_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Photo not found.')
    photo.content = base64.b64encode(photo.content)
    return photo
    # return StreamingResponse(BytesIO(photo.content), media_type="image/jpeg")