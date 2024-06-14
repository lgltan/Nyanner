from pydantic import BaseModel

class User(BaseModel):
    user_type: int
    first_name: str
    last_name: str
    email: str
    username: str
    phone_number: str
    password: str
    photo: str

# NOTE: This is just like serializer.py in django