from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated

from server import auth, lobby, log_utils, models, admin, chess_routes
from server.database import SessionLocal, engine
from server.utils import get_current_user
from server.log_utils import logger, make_log_writable, make_log_read_only


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(lobby.router)
app.include_router(admin.router)
app.include_router(log_utils.router)
app.include_router(chess_routes.router)

# Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]