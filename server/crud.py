from sqlalchemy.orm import Session

from server import models, schemas

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    del user.password
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    del user.password
    return user

# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def get_users(db: Session, skip:int=0, limit:int=100):
#     # return db.query(models.User).offset(skip).limit(limit).all()
#     return db.query(models.User).offset(skip).limit(limit).all()

# def create_user(db: Session, user:schemas.UserCreate):
#     db_user = models.User(email=user.email,
#                           name=user.name)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user