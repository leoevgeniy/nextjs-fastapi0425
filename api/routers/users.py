from datetime import timedelta
from typing import Dict, Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from api.DAO.settings import SettingsDAO
from api.DAO.user import UserDAO
from api.config import settings
from api.auth.auth import (
    authenticate_user, 
    create_access_token, 
    create_reset_password_token, 
    decode_reset_password_token, 
    get_current_user, 
    get_password_hash
)
from api.schema.schema import (
    ForgetPasswordRequest, 
    ResetForegetPassword, 
    SUserProfile, 
    SUserRead, 
    SUserRegister, 
    Token, 
    User
)
import logging

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth & Users"]
)

logger = logging.getLogger(__name__)

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """Аутентификация пользователя и получение токена доступа."""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Уменьшен срок действия токена с 60 дней до 7
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=SUserProfile)
async def read_users_me(current_user: User = Depends(get_current_user)) -> SUserProfile:
    """Получение информации о текущем пользователе."""
    return current_user

@router.post("/register", response_model=Dict[str, Any])
async def register_user(user_data: SUserRegister) -> Dict[str, Any]:
    """Регистрация нового пользователя."""
    # Проверка существующего email и телефона
    if await UserDAO.find_one_or_none(email=user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if await UserDAO.find_one_or_none(phone=user_data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    user = await UserDAO.add(
        first_name=user_data.first_name,
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_password
    )
    
    # Возвращаем пользователя без автоматического входа
    return {
        'user': user,
        'message': 'Registration successful. Please login.'
    }

@router.post("/forget-password")
async def forget_password(
    background_tasks: BackgroundTasks,
    fpr: ForgetPasswordRequest
) -> JSONResponse:
    """Запрос на сброс пароля."""
    try:
        user = await UserDAO.find_one_or_none(email=fpr.email)
        if not user:
            logger.warning(f"Password reset request for non-existent email: {fpr.email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not found"
            )
        
        settings = await SettingsDAO.find_one_or_none(is_active=True)
        if not settings:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error"
            )
        
        secret_token = await create_reset_password_token(email=user.email)
        forget_url_link = f"http://{settings.inputhost}/{settings.forget_password_url}/{secret_token}"
        
        message = MessageSchema(
            subject=f"Восстановление пароля {settings.company_name}",
            recipients=[fpr.email],
            template_body={
                "company_name": settings.company_name,
                "reset_link": forget_url_link
            },
            subtype=MessageType.html
        )
        
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.company_email,
            MAIL_PASSWORD=settings.company_email_password,
            MAIL_FROM=settings.company_email,
            MAIL_PORT=settings.company_email_port,
            MAIL_SERVER=settings.company_email_smtp_server,
            MAIL_FROM_NAME=settings.company_name,
            MAIL_STARTTLS=settings.company_mail_startTLS,
            MAIL_SSL_TLS=settings.company_MAIL_SSL_TLS
        )
        
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message, "mail/password_reset.html")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Password reset email has been sent",
                "success": True
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in password reset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not process password reset request"
        )

@router.post("/reset-password")
async def reset_password(rfp: ResetForegetPassword) -> Dict[str, Any]:
    """Сброс пароля по токену."""
    try:
        # Валидация токена
        token_data = await decode_reset_password_token(token=rfp.secret_token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Проверка совпадения паролей
        if rfp.new_password != rfp.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        
        # Обновление пароля
        user = await UserDAO.find_one_or_none(id=int(token_data['sub']))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        hashed_password = get_password_hash(rfp.new_password)
        await UserDAO.update_by_id(user.id, {"password": hashed_password})
        
        return {
            'success': True,
            'message': 'Password has been reset successfully'
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not reset password"
        )

@router.put("/profile_update")
async def profile_update(
    new_data: SUserRegister,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Обновление профиля пользователя."""
    try:
        updating_data = {
            'first_name': new_data.first_name,
            'email': new_data.email,
            'phone': new_data.phone
        }
        
        if new_data.password:
            updating_data['password'] = get_password_hash(new_data.password)
        
        await UserDAO.update_by_id(current_user.id, updating_data)
        
        return {
            'success': True,
            'message': 'Profile updated successfully'
        }
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update profile"
        )