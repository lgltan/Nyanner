# https://www.youtube.com/watch?v=0A_GCXBCNUQ

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from server.database import SessionLocal
from server.models import User
from passlib.context import CryptContext
from dotenv import load_dotenv
from server.schemas import Photo, CreateUserRequest, LoginRequest, Token, TokenData, UserData
from server.auth import authenticate_user, create_access_token, get_current_active_user, db_dependency, bcrypt_context, TOKEN_EXPIRATION
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