from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

# Used when sending messages from client
class MessageCreate(BaseModel):
    room_id: str
    username: str
    message: str

# Used when returning message from DB
class Message(BaseModel):
    id: int
    room_id: str
    username: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True
