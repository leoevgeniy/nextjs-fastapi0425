from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
import jwt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from api.DAO.user import UserDAO
from api.config import settings
from passlib.context import CryptContext
from api.schema.schema import TokenData
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import logging
from fastapi.security import SecurityScopes

# Настройка логирования
logger = logging.getLogger(__name__)

# Конфигурация хеширования паролей
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=60000  # Увеличено количество раундов
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

def get_password_hash(password: str) -> str:
    """Хеширование пароля."""
    return pwd_context.hash(password)  # Используем hash вместо encrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля."""
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(security_scopes: SecurityScopes, token: Optional[str] = Depends(oauth2_scheme)) -> Any:
    if not token and not security_scopes.scopes:
        return None  # Разрешаем анонимный доступ
    """Получение текущего пользователя по JWT токену."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("security_scopes.scopes", security_scopes.scopes)
    if security_scopes.scopes:
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]  # Алгоритм как список
            )
            print("payload", payload)
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id)
        except jwt.ExpiredSignatureError:
            print('Token has expired')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token attempt: {e}")
            raise credentials_exception
        
        user = await UserDAO.find_one_or_none(id=token_data.user_id)
        if user is None:
            logger.warning(f"User not found for token: {user_id}")
            raise credentials_exception
            # return None
        return user
    else:
        # Guest user path
        return None

async def authenticate_user(email: str, password: str) -> Optional[Any]:
    """Аутентификация пользователя."""
    user = await UserDAO.find_one_or_none(email=email)
    if not user:
        logger.warning(f"Login attempt for non-existent user: {email}")
        return None
    if not verify_password(password, user.password):
        logger.warning(f"Invalid password attempt for user: {email}")
        return None
    return user

def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Создание JWT токена."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=30))  # Увеличено до 30 мин
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )

async def create_reset_password_token(email: str) -> Optional[str]:
    """Создание токена для сброса пароля."""
    user = await UserDAO.find_one_or_none(email=email)
    if not user:
        logger.warning(f"Password reset attempt for non-existent email: {email}")
        return None
    data = {"sub": str(user.id), "exp": datetime.now(timezone.utc) + timedelta(minutes=60)}
    return jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)

async def decode_reset_password_token(token: str) -> Dict[str, Any]:
    """Декодирование токена сброса пароля."""
    try:
        return jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password reset token has expired"
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid password reset token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password reset token"
        )

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user = await UserDAO.find_one_or_none(email=username)
        
        if not user or not user.is_superuser or not verify_password(password, user.password):
            return False
        access_token_expires = timedelta(days=60)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        # Validate username/password credentials
        # And update session
        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)