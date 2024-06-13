from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from server import crud, models, schemas, auth
from server.database import SessionLocal, engine
from server.auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)

# Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.post("/", response_model=schemas.User)
def post_user(user: user_dependency, db: db_dependency):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db,user=user)

@app.get("/", response_model=list[schemas.User])
def get_users(skip:int=0, limit:int=0, db:Session=Depends(get_db)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users

@app.get("/{user_id}/", response_model=schemas.User)
def get_user(user_id:int, db: db_dependency):
    db_user = crud.get_user(db,user_id =user_id )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user