from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, TIMESTAMP, Text
from api.database.database import Base
from enum import Enum

class SessionInfo(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    session_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_guest = Column(Boolean, default=False)  # Add this field
    
class MessageInfo(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("session.id"), nullable=True)
    role = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    is_guest = Column(Boolean, default=False)  # Add this field