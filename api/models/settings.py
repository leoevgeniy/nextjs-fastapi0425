from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from api.database.database import Base


storage = FileSystemStorage(path="static")

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True )
    company_name = Column(String, nullable=False, unique=True)
    company_url = Column(String, default="example.com")
    company_email_smtp_server = Column(String, nullable=False)
    company_email_port = Column(Integer, nullable=False, default=465)
    company_mail_startTLS = Column(Boolean, nullable=False, default=False)
    company_MAIL_SSL_TLS = Column(Boolean, nullable=False, default=True)
    company_email = Column(String, nullable=False, unique=True)
    company_email_password = Column(String, nullable=False, unique=True)
    company_phone = Column(String, nullable=False, unique=True)
    company_address = Column(String, nullable=False, unique=True)
    company_logo = Column(FileType(storage=storage), nullable=False)
    products_update_feed = Column(String, nullable=True, default='input url')
    inputhost = Column(String, nullable=False, default="127.0.0.1")
    forget_password_url = Column(String, nullable=False, default="forget_password")
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now)
    
    class Config:
        orm_mode = True
        
class SiteOrder(Base):
    __tablename__ = 'siteorder'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    name = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    comment = Column(String, nullable=True)