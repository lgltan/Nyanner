# https://www.youtube.com/watch?v=0A_GCXBCNUQ

from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from starlette import status
from server.models import AdminLog, User, Photo, Session as UserSession
from dotenv import load_dotenv
from server.schemas import CreateUserRequest, LoginRequest, Token, UserData, PhotoData
from server.utils import validate_image, validate_phone_number, validate_name, validate_user_data, authenticate_user, create_access_token, get_current_active_user, get_current_user, db_dependency, bcrypt_context, TOKEN_EXPIRATION
import base64

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
                        birthday: str = Form(...),
                        user_password: str = Form(...),
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
        birthday=birthday,
        user_password=user_password,
        confirm_password=confirm_password
    )
    
    if not create_user_request.username or not create_user_request.first_name or not create_user_request.last_name or not create_user_request.email or not create_user_request.phone_number or not create_user_request.user_password or not create_user_request.confirm_password or not file:
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
        birthday=create_user_request.birthday,
        photo_id=photo_id,
        user_password=bcrypt_context.hash(create_user_request.user_password).encode('ascii'),
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
    user = authenticate_user(request.username, request.user_password, db)
    
    if not user:
        # Log the failed login attempt
        admin_log = AdminLog(admin_description=f"Failed login attempt for username: {request.username}")
        db.add(admin_log)
        db.commit()

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
    
    user_session = db.query(UserSession).filter(UserSession.user_id == user.user_id).first()
    if user_session and user_session.ban_bool:
        ban_end_time = user_session.ban_timestamp + timedelta(minutes=user_session.ban_time)
        if datetime.now() < ban_end_time:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is banned",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            user_session.ban_bool = False
            # Log the successful login attempt
            admin_log = AdminLog(admin_description=f"Successful login for username: {request.username}")
            db.add(admin_log)
            db.commit()

    access_token_expires = None
    if request.rememberMe:
        access_token_expires = timedelta(days=int(TOKEN_EXPIRATION))
    access_token = create_access_token(user.username, user.user_id, user.user_type, access_token_expires)

    return Token(access_token=access_token, token_type='bearer')
    
@router.get('/users/me', response_model=UserData)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return { 
        'user_id': current_user['user'].user_id,
        'user_type': current_user['user'].user_type,
        'username': current_user['user'].username,
        'first_name': current_user['user'].first_name,
        'last_name': current_user['user'].last_name,
        'email': current_user['user'].email,
        'phone_number': current_user['user'].phone_number,
        'birthday': current_user['user'].birthday,
        'photo_id': current_user['user'].photo_id,
        'photo': current_user['photo']
    }

@router.get("/photos/{photo_id}", response_model=PhotoData)
async def get_photo(db: db_dependency, photo_id: int):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Photo not found.')
    photo.content = base64.b64encode(photo.content).decode('ascii')
    return {'id': photo.id, 'filename': photo.filename, 'content': photo.content}

@router.put('/edit/me', status_code=status.HTTP_200_OK)
async def edit_user(
    db: db_dependency,
    username: str,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
):
    # Ensure the user can only edit their own profile
    if current_user['user'].username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this user")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if first_name:
        if not validate_name(first_name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid first name')
        user.first_name = first_name.encode('ascii')
    if last_name:
        if not validate_name(last_name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid last name')
        user.last_name = last_name.encode('ascii')
    if phone_number:
        if not validate_phone_number(phone_number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid phone number')
        user.phone_number = phone_number.encode('ascii')

    # Handle photo upload
    if file:
        FILE_SIZE_LIMIT = 5 * 1024 * 1024  # 5MB
        if file.size > FILE_SIZE_LIMIT:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File size too large')
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file type')
        if not validate_image(file):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid image file')

        photo_content = file.file.read()
        photo = Photo(filename=file.filename, content=photo_content)
        db.add(photo)
        db.commit()
        db.refresh(photo)
        user.photo_id = photo.id

    db.commit()
    db.refresh(user)

    admin_log = AdminLog(admin_description=f"Successfully edited profile for username: {user.username}")
    db.add(admin_log)
    db.commit()
    
    return {"message": "User details updated successfully"}

@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(db: db_dependency, current_user: dict = Depends(get_current_user)):
    username = current_user['user'].username
    try:
        admin_log = AdminLog(admin_description=f"Successfully logged out for username: {username}")
        db.add(admin_log)
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to log out {username}")
    
    # return {"message": "User logged out successfully"}