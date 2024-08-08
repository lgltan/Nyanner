from fastapi import FastAPI, Depends,  HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from server.utils import debug_mode

from server import auth, lobby, log_utils, models, admin
from server.database import SessionLocal, engine
from server.utils import get_current_user

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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if not debug_mode():
        return RedirectResponse(url="/brokenpage", status_code=status.HTTP_200_OK)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if not debug_mode():
        return RedirectResponse(url="/brokenpage", status_code=status.HTTP_200_OK)
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

# Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]