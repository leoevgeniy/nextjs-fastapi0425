import httpx
from typing import Optional
from gigachat import GigaChat
from gigachat.models import Chat, Messages
from api.middleware import logger
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    DATABASE_URL = "sqlite:///chat.db"
    GIGA_CHAT_TIMEOUT = 30
    RATE_LIMITS = {
        "register": "5/minute",
        "login": "10/minute",
        "chat": "15/minute",
        "history": "30/minute"
    }

# Инициализация GigaChat
class GigaChatService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = GigaChat(
                credentials=os.getenv("GIGACHAT_TOKEN"),
                ca_bundle_file="./api/routers/russian_trusted_root_ca.cer",
                verify_ssl_certs=True,
                timeout=Config.GIGA_CHAT_TIMEOUT
            )
        return cls._instance
    
    def get_chat_stream(self, messages: list[Messages]):
        try:
            return self.client.stream(Chat(messages=messages))
        except Exception as e:
            logger.error(f"GigaChat error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Chat service unavailable"
            )
