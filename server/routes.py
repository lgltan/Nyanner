# https://www.youtube.com/watch?v=0A_GCXBCNUQ

from datetime import timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import User, Photo, Lobby
from passlib.context import CryptContext
from dotenv import load_dotenv
from server.schemas import CreateUserRequest, LoginRequest, Token, TokenData, UserData, CreateLobbyRequest
from server.auth import validate_image, validate_user_data, authenticate_user, create_access_token, get_current_active_user, db_dependency, bcrypt_context, TOKEN_EXPIRATION
import os

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

###############
##  ROUTES   ##
###############
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                        username: str = Form(...),
                        first_name: str = Form(...),
                        last_name: str = Form(...),
                        email: str = Form(...),
                        phone_number: str = Form(...),
                        password: str = Form(...),
                        confirm_password: str = Form(...),
                        file: Optional[UploadFile] = File(None)
    ):

    create_user_request = CreateUserRequest(
        user_type=0,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password=password,
        confirm_password=confirm_password
    )
    
    if not create_user_request.username or not create_user_request.first_name or not create_user_request.last_name or not create_user_request.email or not create_user_request.phone_number or not create_user_request.password or not create_user_request.confirm_password or not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Please fill out all fields."})
    
    # Validate information
    errors = validate_user_data(db, create_user_request, file)
    
    if len(errors) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors)
    
    # Handle photo upload
    photo_id = None
    if file:
        photo_content = file.file.read()
        photo = Photo(filename=file.filename, content=photo_content)
        db.add(photo)
        db.commit()
        db.refresh(photo)
        photo_id = photo.id
    
    new_user = User(
        user_type=0,
        username=create_user_request.username.encode('ascii'),
        first_name=create_user_request.first_name.encode('ascii'),
        last_name=create_user_request.last_name.encode('ascii'),
        email=create_user_request.email.encode('ascii'),
        phone_number=create_user_request.phone_number.encode('ascii'),
        photo_id=photo_id,
        password=bcrypt_context.hash(create_user_request.password).encode('ascii'),
    )
    
    db.add(new_user)
    db.commit()

@router.post('/uploadfile', status_code=status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No file uploaded.')
    
    FILE_SIZE_LIMIT = 5 * 1024 * 1024   # 5MB
    if file.size > FILE_SIZE_LIMIT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File size too large.')
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file type.')
    
    if not validate_image(file):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid image file.')
    

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

@router.post('/lobby', status_code=status.HTTP_201_CREATED)
async def create_lobby(db: db_dependency, 
                        lobby_name: str = Form(...),
                        p1_id: str = Form(...),
    ):

    create_lobby_request = CreateLobbyRequest(
        lobby_name="",
        p1_id="",
        
    )
    
    if not create_lobby_request.lobby_name or not create_lobby_request.p1_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"general": "Please fill out all fields."})

    new_lobby = Lobby(
        lobby_name=create_lobby_request.lobby_name.encode('ascii'),
        p1_id=create_lobby_request.p1_id.encode('ascii'),
    )
    
    db.add(new_lobby)
    db.commit()