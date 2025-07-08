import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, EmailStr
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: int | None = None
    
class User(BaseModel):
    first_name: str
    email: EmailStr
    phone: str
    
class SUserRegister(BaseModel):
    first_name: str
    email: EmailStr
    phone: str
    password: str
    
class SUserAuthByEmail(BaseModel):
    email: EmailStr
    password: str


class SUserRead(BaseModel):
    first_name: str
    email: EmailStr
    phone: str


class SUserProfile(BaseModel):
    first_name: str
    email: EmailStr
    phone: str
    tokens_remain: int
    balance: int
    discount: int
    
class SRegisteredUser(BaseModel):
    user: SUserRead
    token: Token


class ForgetPasswordRequest(BaseModel):
    email: str


class ResetForegetPassword(BaseModel):
    secret_token: str
    new_password: str
    confirm_password: str
    
class Product(BaseModel):
    aID: int
    prodID: int
    productName: str
    vendor: str
    userPrice: float
    retailPrice: float
    discount: int
    stock: int
    shippingDate: Optional[str] = None
    description: str
    category2: str
    category3: str
    genderSpecific: Optional[int] = None
    images: str
    collection: str
    
class Size(BaseModel):
    size: str
    stock: int
    aID: int
    image: str   
    color: str
    
    
class Color(BaseModel):
    color: str
    colorUrl: str
    sizes: list[Size]   
    
class ProductIndex(BaseModel):
    aID: int
    prodID: int
    productName: Optional[str] = None
    vendor: str
    userPrice: float
    retailPrice: float
    discount: int
    stock: int
    shippingDate: Optional[str] = None
    description: str
    category2: str
    category3: str
    genderSpecific: Optional[int] = None
    images: str
    colors: list[Color]
    collection: Optional[str] = ''

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class SessionInfo(BaseModel):
    id: str
    name: str
    created_at: str
    last_activity: str

class MessageInfo(BaseModel):
    role: str
    content: str
    timestamp: str
    
class SessionInfoResponse(BaseModel):
    id: int
    user_id: int
    name: str
    created_at: datetime.datetime
    last_activity: Optional[datetime.datetime] = None  # Добавляем поле для последней активности

    class Config:
        from_attributes = True  # Ранее known as orm_mode
        
class MessageInfoResponse(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True  # Для работы с ORM
        
class RenameSessionRequest(BaseModel):
    new_name: str