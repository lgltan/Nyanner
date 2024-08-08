import logging
from logging.handlers import RotatingFileHandler
import os
import shutil
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
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
    try:
        make_log_writable(log_file)
        logger.log(logging.getLevelName(level), message)
        log_to_db(db, message, level)
        make_log_read_only(log_file)
    except Exception as e:
        print(f"Logging failed: {e}")

def delete_file(file_path: str):
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {file_path}, {e}")

router = APIRouter(
    prefix='/logs',
    tags=['logs']
)

@router.get("/copy_and_download_log", response_class=FileResponse)
async def copy_and_download_log(background_tasks: BackgroundTasks, db: db_dependency):
    try:
        copied_log_file = "app_copy.log"
        # Copy the log file
        shutil.copy(log_file, copied_log_file)

        # Check if the copied log file exists
        if not os.path.exists(copied_log_file):
            raise HTTPException(status_code=404, detail="Copied log file not found")
        
        # Schedule the delete_file function to run after the response is sent
        background_tasks.add_task(delete_file, copied_log_file)

        # Log the download action
        log_message(db, "Log file copy downloaded.")

        # Return the copied log file for download
        return FileResponse(copied_log_file, media_type='application/octet-stream', filename='app_copy.log')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while copying or downloading the log file: {str(e)}")
