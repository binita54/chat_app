from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base

# ✅ User model (same as yours, improved with relationship)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")  # 'user' or 'admin'

    messages = relationship("Message", back_populates="sender")

# ✅ Room model (newly added)
class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    messages = relationship("Message", back_populates="room")

# ✅ Message model (your original code + improved)
class Message(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))  # changed to FK
    sender_id = Column(Integer, ForeignKey("users.id"))  # new: FK for username/user

    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    sender = relationship("User", back_populates="messages")
    room = relationship("Room", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
