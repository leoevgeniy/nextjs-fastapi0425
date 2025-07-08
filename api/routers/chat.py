import json
import uuid
from fastapi import APIRouter,  Depends, HTTPException, Request, status, Path
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from api.schema.schema import ChatRequest, MessageInfoResponse, RenameSessionRequest, SessionInfo, MessageInfo, SessionInfoResponse
from api.middleware import limiter
from api.auth.auth import get_current_user
from api.services.gigachat import GigaChatService, Config
from api.database.database import async_session
from gigachat.models import Messages
import datetime
import logging
from sqlalchemy import select
from api.schema.schema import ChatRequest  # Pydantic-модель
from api.models.session import SessionInfo, MessageInfo  # SQLAlchemy-модели


router = APIRouter(
    prefix="/api/chat",
    tags=["AI Chat"]
)

logger = logging.getLogger(__name__)

@router.post("/api/chat-stream")
@limiter.limit(Config.RATE_LIMITS["chat"])
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,  # ← Pydantic-модель (только для валидации)
    current_user: dict = Depends(get_current_user),
):
    
    async def generate():
        try:
            async with async_session() as session:
                # ===== 1. Управление сессией =====
                if not chat_request.session_id:
                    # Создаём новую сессию (используем SQLAlchemy-модель!)
                    session_id = str(uuid.uuid4())
                    new_session = SessionInfo(
                        session_id=session_id,
                        user_id=current_user.id,
                        name="New Chat",
                        created_at=datetime.datetime.now()
                    )
                    session.add(new_session)
                    await session.commit()
                else:
                    # Проверяем существующую сессию
                    existing_session = await session.execute(
                        select(SessionInfo)
                        .where(SessionInfo.session_id == chat_request.session_id)
                    )
                    result = existing_session.scalars().one_or_none()
                    print(result.user_id, current_user.id)
                    if not existing_session or result.user_id != current_user.id:
                        yield "data: {\"error\": \"Invalid session\"}\n\n"
                        yield "data: [DONE]\n\n"
                        return
                    session_id = chat_request.session_id

                # ===== 2. Сохраняем сообщение пользователя =====
                # Важно: используем SQLAlchemy-модель MessageInfo, а не ChatRequest!
                user_message = MessageInfo(
                    session_id=session_id,
                    role="user",
                    content=chat_request.message,  # ← берём текст из Pydantic-модели
                    created_at=datetime.datetime.now()
                )
                session.add(user_message)
                await session.commit()

                # ===== 3. Получаем историю сообщений =====
                history = (await session.execute(
                    select(MessageInfo)
                    .where(MessageInfo.session_id == session_id)
                    .order_by(MessageInfo.created_at.asc())
                    .limit(10)
                )).scalars().all()

                # ===== 4. Отправляем запрос в GigaChat =====
                messages_for_giga = [
                    Messages(role=msg.role, content=msg.content)  # ← совместимый с GigaChat формат
                    for msg in history
                ]
                
                giga = GigaChatService()
                full_response = ""
                try:
                    # # Вариант 1: если get_chat_stream стал асинхронным
                    # async for chunk in giga.get_chat_stream(messages_for_giga):
                    #     if chunk.choices and chunk.choices[0].delta.content:
                    #         content = chunk.choices[0].delta.content
                    #         full_response += content
                    #         yield f"data: {json.dumps({'content': content})}\n\n"

                    # ИЛИ Вариант 2: если оставляете синхронный генератор
                    for chunk in giga.get_chat_stream(messages_for_giga):
                        if chunk.choices and chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            yield f"data: {json.dumps({'content': content})}\n\n"
                except Exception as e:
                    logger.error(f"GigaChat error: {e}")
                    raise

                # ===== 5. Сохраняем ответ AI =====
                ai_message = MessageInfo(
                    session_id=session_id,
                    role="assistant",
                    content=full_response,
                    created_at=datetime.datetime.now()
                )
                session.add(ai_message)
                await session.commit()

                yield "data: [DONE]\n\n"
                yield f"event: session_id\ndata: {session_id}\n\n"

        except Exception as e:
            logger.error(f"Chat error: {e}", exc_info=True)
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/api/history", response_model=list[SessionInfoResponse])
@limiter.limit(Config.RATE_LIMITS["history"])
async def get_history(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with async_session() as session:
        # Правильное построение запроса с outerjoin
        query = (
            select(
                SessionInfo,
                func.max(MessageInfo.created_at).label("last_activity")
            )
            .select_from(SessionInfo)
            .outerjoin(MessageInfo, SessionInfo.session_id == MessageInfo.session_id)
            .where(SessionInfo.user_id == current_user.id)
            .group_by(SessionInfo.session_id)
            .order_by(func.max(MessageInfo.created_at).desc())
        )
        
        sessions = await session.execute(query)
        
        # Преобразуем результаты в Pydantic-модели
        result = []
        for session_info, last_activity in sessions:
            session_data = SessionInfoResponse.from_orm(session_info)
            session_data.last_activity = last_activity
            result.append(session_data)
            
        return result
    
@router.get("/api/history/{session_id}", response_model=list[MessageInfoResponse])
@limiter.limit(Config.RATE_LIMITS["history"])
async def get_session_messages(
    request: Request,
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    async with async_session() as session:
        # Проверка принадлежности сессии пользователю
        session_exists = await session.execute(
            select(MessageInfo)
            .where(MessageInfo.session_id == session_id)
            .order_by(MessageInfo.created_at.desc())
            .limit(100)  # Последние 100 сообщений
        )
        if not session_exists.scalars().first():
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Получаем сообщения
        messages = await session.execute(
            select(MessageInfo)
            .where(MessageInfo.session_id == session_id)
            .order_by(MessageInfo.created_at)
        )
        
        # Преобразуем в Pydantic-модели
        return [
            MessageInfoResponse.from_orm(msg) 
            for msg in messages.scalars().all()
        ]
        
@router.patch("/api/history/{session_id}/rename", response_model=SessionInfoResponse)
@limiter.limit(Config.RATE_LIMITS["history"])
async def rename_session(
    request: Request,
    session_id: str = Path(..., description="ID сессии для переименования"),
    rename_data: RenameSessionRequest = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Переименовывает существующую сессию чата.
    Требуется аутентификация и принадлежность сессии пользователю.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not rename_data or not rename_data.new_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New name is required"
        )

    async with async_session() as session:
        # 1. Проверяем существование сессии и принадлежность пользователю
        session_to_rename = await session.execute(
            select(SessionInfo)
            .where(
                SessionInfo.session_id == session_id,
                SessionInfo.user_id == current_user.id
            )
        )
        session_to_rename = session_to_rename.scalars().first()
        
        if not session_to_rename:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or access denied"
            )

        # 2. Обновляем имя сессии
        session_to_rename.name = rename_data.new_name[:100]  # Ограничиваем длину имени
        session.add(session_to_rename)
        await session.commit()
        await session.refresh(session_to_rename)

        # 3. Возвращаем обновлённую сессию
        return SessionInfoResponse.from_orm(session_to_rename)

