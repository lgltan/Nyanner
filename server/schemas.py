from pydantic import BaseModel
from server.auth import Photo

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    phone_number: str
    password: str
    # photo: Photo

# NOTE: This is just like serializer.py in django