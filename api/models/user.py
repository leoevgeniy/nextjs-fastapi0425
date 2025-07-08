from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, TIMESTAMP, Text
from api.database.database import Base
from enum import Enum

class UserRole(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ADMIN = "admin"
    
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    balance = Column(Integer, nullable=True, default=0)
    tokens_remain = Column(Integer, nullable=True, default=10)
    discount = Column(Integer, nullable=True, default=0)
    registered_at = Column(TIMESTAMP, default=datetime.now)
    password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    is_superuser: bool = Column(Boolean, nullable=False, default=False)
    is_verified: bool = Column(Boolean, nullable=False, default=False)
    
    class Config:
        orm_mode = True
        
class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    prompt = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

