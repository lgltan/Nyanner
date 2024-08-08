import logging
from logging.handlers import RotatingFileHandler
import os
import shutil
from fastapi import APIRouter, HTTPException, Depends
from server.models import AdminLog
from datetime import datetime
from server.utils import db_dependency

# Create a logger
logger = logging.getLogger("nyanner")
logger.setLevel(logging.INFO)

log_file = "app.log"

def ensure_log_file_writable(log_file):
    if not os.path.exists(log_file):
        open(log_file, 'a').close()
    os.chmod(log_file, 0o666)  # Set the file to writable

# Ensure the log file is writable at the start
ensure_log_file_writable(log_file)

# Create a file handler that logs messages to a file
log_file = "app.log"
file_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)
file_handler.setLevel(logging.INFO)

# Create a console handler that logs messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Function to make the log file read-only
def make_log_read_only(log_file):
    os.chmod(log_file, 0o444)  # Set the log file to read-only

# Function to make the log file writable
def make_log_writable(log_file):
    os.chmod(log_file, 0o666)  # Set the log file to writable

def log_to_db(db: db_dependency, message: str, level: str = 'INFO'):
    log_entry = AdminLog(admin_description=message, admin_timestamp=datetime.now())
    db.add(log_entry)
    db.commit()

def log_message(db: db_dependency, message: str, level: str = 'INFO'):
    make_log_writable(log_file)
    logger.log(logging.getLevelName(level), message)
    log_to_db(db, message, level)
    make_log_read_only(log_file)

router = APIRouter(
    prefix='/logs',
    tags=['logs']
)

# Endpoint to request a copy of the log file
@router.post("/request_log_copy")
async def request_log_copy():
    try:
        src_file = "app.log"
        dst_file = "app_copy.log"
        shutil.copy(src_file, dst_file)
        return {"message": "Log file copied successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while copying the log file: {str(e)}")

# Example usage of logging
@router.get("/")
async def root():
    make_log_writable(log_file)  # Ensure the log file is writable before logging
    logger.info("Root endpoint accessed")
    make_log_read_only(log_file)  # Make the log file read-only after logging
    return {"message": "Hello, World!"}
