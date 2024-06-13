from sqlalchemy.orm import Session

from server import models,schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip:int=0, limit:int=100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user:schemas.UserCreate):
    db_user = models.User(email=user.email,
                          name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# NOTE :
# - add that instance object to your database session.
# - commit the changes to the database (so that they are saved).
# - refresh your instance (so that it contains any new data from the database, like the generated ID).