from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from server.models import AdminLog, User, Photo, BannedUsers, IssuedToken
from dotenv import load_dotenv
from server.schemas import CreateUserRequest, LoginRequest, Token, UserData, PhotoData
from server.utils import add_photo, get_captcha_secret_key, get_captcha_site_key, validate_image, validate_phone_number, validate_name, validate_user_data, validate_birthday, authenticate_user, create_access_token, get_current_active_user, get_current_user, get_photo_from_db, db_dependency, bcrypt_context, TOKEN_EXPIRATION, debug_mode, handle_error
from server.log_utils import make_log_read_only, make_log_writable, log_message
import base64
import httpx

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
        # photo_content = file.file.read()
        # photo = Photo(filename=file.filename, content=photo_content)
        # db.add(photo)
        # db.commit()
        # db.refresh(photo)
        # photo_id = photo.id
        photo_id = await add_photo(file, db)
    
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
    db.refresh(new_user)
    user_id = new_user.user_id

    if user_id:
        log_message(db, f"Successfully registerd user: {new_user.username}")
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

@router.post("/login", response_model=Token)
async def login_for_access_token(
    request: LoginRequest,
    db: db_dependency
) -> Token:
    try:
        async with httpx.AsyncClient() as client:
            recaptcha_response = await client.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data={
                    'secret': get_captcha_secret_key(),
                    'response': request.recaptchaToken
                }
            )
        
        recaptcha_result = recaptcha_response.json()

        if not recaptcha_result.get('success'):
            log_message(db, f"Failed login attempt for username: {request.username}. Invalid reCAPTCHA token.")
            db.commit()
            raise ValueError("Invalid reCAPTCHA token")

        user = authenticate_user(request.username, request.user_password, db)
        
        if not user:
            log_message(db, f"Failed login attempt for username: {request.username}. Invalid credentials.")
            db.commit()
            raise ValueError("Invalid Credentials")
        
        banned_user = db.query(BannedUsers).filter(BannedUsers.key_to_user_id == user.user_id).first()
        if banned_user and banned_user.ban_bool:
            ban_end_time = banned_user.ban_timestamp + timedelta(minutes=banned_user.ban_time)
            if datetime.now() < ban_end_time:
                ban_duration = ban_end_time - datetime.now()
                log_message(db, f"Failed login attempt for username: {request.username}. User is banned for {ban_duration}.")
                db.commit()
                raise ValueError("User is banned")
            else:
                banned_user.ban_bool = False
                banned_user.ban_timestamp = None
                banned_user.ban_time = 0
        
        log_message(db, f"Successful login for username: {request.username}")
        db.commit()

        access_token_expires = None
        if request.rememberMe:
            access_token_expires = timedelta(minutes=int(TOKEN_EXPIRATION))
        issued_at, access_token = create_access_token(user.username, user.user_id, user.user_type, access_token_expires)

        issued_token = IssuedToken(token_id=access_token, user_id=user.user_id, issued_at=issued_at)
        db.add(issued_token)
        db.commit()

        return Token(access_token=access_token, token_type='bearer')
    except Exception as exc:
        handle_error(exc, message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)
    
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
    try:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise ValueError("Photo not found.")
        photo.content = base64.b64encode(photo.content).decode('ascii')
        return {'id': photo.id, 'filename': photo.filename, 'content': photo.content}
    except Exception as exc:
        handle_error(exc, message="Photo not found", status_code=status.HTTP_404_NOT_FOUND)

@router.put('/edit/me', status_code=status.HTTP_200_OK)
async def edit_user(
    db: db_dependency,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    birthday: Optional[datetime] = Form(None),
    confirm_password: str = Form(None),
    current_user: User = Depends(get_current_user),
):
    username = current_user['user'].username
    if not username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No username provided")
    
    user = authenticate_user(username, confirm_password, db)
    if not user:
        log_message(db, f"Failed UPDATE attempt for username: {username}")
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'general': 'Invalid password'})

    isChanged = False

    if first_name and not str(first_name) == str(user.first_name):
        if not validate_name(first_name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'firstName': 'Invalid first name'})
        user.first_name = first_name
        isChanged = True
    
    if last_name and not str(last_name) == str(user.last_name):
        if not validate_name(last_name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'lastName': 'Invalid last name'})
        user.last_name = last_name
        isChanged = True

    if phone_number and not str(phone_number) == str(user.phone_number):
        if not validate_phone_number(phone_number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'phoneNumber': 'Invalid phone number'})
        user.phone_number = phone_number
        isChanged = True

    if birthday and not birthday.strftime("%m/%d/%Y") == user.birthday.strftime("%m/%d/%Y"):
        if not validate_birthday(birthday):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'birthday': 'Invalid birthday'})
        user.birthday = birthday
        isChanged = True

    if file != None:
        old_photo = await get_photo_from_db(user.photo_id, db)
        if file.filename != old_photo.filename:
            if not validate_image(file):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'profilePhoto': 'Invalid image file'})
            
            user.photo_id = await add_photo(file, db)

    if isChanged:
        db.commit()
        db.refresh(user)

        log_message(db, f"Successfully edited profile for username: {user.username}")
        db.commit()
    else:
        log_message(db, f"No changes for username: {user.username}")
        db.commit()
    
    return {"message": "User details updated successfully"}

@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(db: db_dependency, current_user: dict = Depends(get_current_user)):
    try:
        username = current_user['user'].username

        # Invalidate token in database
        issued_token = db.query(IssuedToken)\
                        .filter(IssuedToken.user_id == current_user['user'].user_id)\
                        .order_by(IssuedToken.issued_at.desc())\
                        .first()
        
        issued_token.invalidated = True
        db.commit()
        db.refresh(issued_token)

        # Log the successful logout
        log_message(db, f"Successfully logged out for username: {username}")
        db.commit()

    except Exception as exc:
        log_message(db, f"Failed logout for username: {username}")
        db.commit()
        handle_error(exc, message=f"Failed to log out {username}", status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/recaptcha', status_code=status.HTTP_200_OK)
async def recaptcha():
    try:
        return {"site_key": get_captcha_site_key()}
    except Exception as exc:
        handle_error(exc, message="Failed to get reCAPTCHA site key", status_code=status.HTTP_400_BAD_REQUEST)
