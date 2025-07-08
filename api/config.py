import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "./api/database.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    INPUTHOST: str = os.getenv("INPUTHOST", "127.0.0.1")
    FORGET_PASSWORD_URL: str = os.getenv("FORGET_PASSWORD_URL")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    GIGACHAT_TOKEN: str = os.getenv("GIGACHAT_TOKEN")

settings = Settings()