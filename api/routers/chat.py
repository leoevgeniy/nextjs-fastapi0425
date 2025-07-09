import json
from typing import Optional
import uuid
from fastapi import APIRouter,  Depends, HTTPException, Request, Response, status, Path
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
from fastapi import Security


router = APIRouter(
    prefix="/api/chat",
    tags=["AI Chat"]
)

logger = logging.getLogger(__name__)

# Track guest sessions and their question counts
guest_sessions = {}

def get_guest_session_id(request: Request) -> str:
    """Generate or get guest session ID based on client IP"""
    client_ip = request.client.host
    if client_ip not in guest_sessions:
        guest_sessions[client_ip] = {
            'session_id': str(uuid.uuid4()),
            'question_count': 0,
            'last_activity': datetime.datetime.now()
        }
    return guest_sessions[client_ip]

def check_guest_limit(request: Request):
    """Check if guest has exceeded question limit"""
    client_ip = request.client.host
    if client_ip in guest_sessions:
        if guest_sessions[client_ip]['question_count'] >= 10:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Guest limit exceeded. Please register to continue."
            )

@router.post("/chat-stream")
@limiter.limit(Config.RATE_LIMITS["chat"])
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,
    current_user: Optional[dict] = Security(get_current_user, scopes=[])
):
    session_id = ''
    # Гостевой доступ
    if current_user is None:
        guest_data = get_guest_session_id(request)
        if guest_data['question_count'] >= 10:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Guest limit exceeded. Please register to continue."
            )
        guest_data['question_count'] += 1
        
        session_id = guest_data['session_id']
        print("session_id", session_id)
        async with async_session() as session:
            # Проверяем/создаем сессию
            existing_session = await session.execute(
                select(SessionInfo).where(SessionInfo.session_id == session_id)
            )
            if not existing_session.scalars().first():
                new_session = SessionInfo(
                    session_id=session_id,
                    user_id=None,
                    name="Guest Session",
                    created_at=datetime.datetime.now(),
                    is_guest=True
                )
                session.add(new_session)
                await session.commit()
        
        # Продолжаем обработку как для гостя
        current_user = {"id": None, "is_guest": True}
    async def generate():
        try:
            async with async_session() as session:
                # ===== Handle Guest Users =====
                if current_user['is_guest']:
                    guest_data = get_guest_session_id(request)
                    check_guest_limit(request)
                    
                    session_id = guest_data['session_id']
                    guest_data['question_count'] += 1
                    guest_data['last_activity'] = datetime.datetime.now()
                    
                    # Create session if not exists
                    existing_session = await session.execute(
                        select(SessionInfo)
                        .where(SessionInfo.session_id == session_id)
                    )
                    if not existing_session.scalars().first():
                        new_session = SessionInfo(
                            session_id=session_id,
                            user_id=None,  # Null for guest sessions
                            name="Guest Chat",
                            created_at=datetime.datetime.now(),
                            is_guest=True
                        )
                        session.add(new_session)
                        await session.commit()
                
                # ===== Handle Authenticated Users =====
                else:
                    if not chat_request.session_id:
                        session_id = str(uuid.uuid4())
                        new_session = SessionInfo(
                            session_id=session_id,
                            user_id=current_user.id,
                            name="New Chat",
                            created_at=datetime.datetime.now(),
                            is_guest=False
                        )
                        session.add(new_session)
                        await session.commit()
                    else:
                        existing_session = await session.execute(
                            select(SessionInfo)
                            .where(SessionInfo.session_id == chat_request.session_id)
                        )
                        result = existing_session.scalars().first()
                        if not result or (result.user_id and result.user_id != current_user.id):
                            yield "data: {\"error\": \"Invalid session\"}\n\n"
                            yield "data: [DONE]\n\n"
                            return
                        session_id = chat_request.session_id

                # ===== Save Message =====
                user_message = MessageInfo(
                    session_id=session_id,
                    role="user",
                    content=chat_request.message,
                    created_at=datetime.datetime.now(),
                    is_guest=not bool(current_user)
                )
                session.add(user_message)
                await session.commit()

                # ===== Get Message History =====
                history = (await session.execute(
                    select(MessageInfo)
                    .where(MessageInfo.session_id == session_id)
                    .order_by(MessageInfo.created_at.asc())
                    .limit(10)
                )).scalars().all()

                # ===== Send to GigaChat =====
                messages_for_giga = [
                    Messages(role=msg.role, content=msg.content)
                    for msg in history
                ]
                
                giga = GigaChatService()
                full_response = ""
                try:
                    for chunk in giga.get_chat_stream(messages_for_giga):
                        if chunk.choices and chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            yield f"data: {json.dumps({'content': content})}\n\n"
                except Exception as e:
                    logger.error(f"GigaChat error: {e}")
                    raise

                # ===== Save AI Response =====
                ai_message = MessageInfo(
                    session_id=session_id,
                    role="assistant",
                    content=full_response,
                    created_at=datetime.datetime.now(),
                    is_guest=not bool(current_user)
                )
                session.add(ai_message)
                await session.commit()

                yield "data: [DONE]\n\n"
                yield f"event: session_id\ndata: {session_id}\n\n"

        except HTTPException as he:
            yield f"data: {json.dumps({'error': he.detail})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Chat error: {e}", exc_info=True)
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream", status_code=200, headers={"x-session-id": session_id})

@router.get("/history", response_model=list[SessionInfoResponse])
@limiter.limit(Config.RATE_LIMITS["history"])
async def get_history(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    session_id = ''
    # Гостевой доступ
    if current_user is None:
        guest_data = get_guest_session_id(request)
        if guest_data['question_count'] >= 10:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Guest limit exceeded. Please register to continue."
            )
        guest_data['question_count'] += 1
        
        session_id = guest_data['session_id']
        print("session_id", session_id)
        async with async_session() as session:
            # Проверяем/создаем сессию
            existing_session = await session.execute(
                select(SessionInfo).where(SessionInfo.session_id == session_id)
            )
            if not existing_session.scalars().first():
                new_session = SessionInfo(
                    session_id=session_id,
                    user_id=None,
                    name="Guest Session",
                    created_at=datetime.datetime.now(),
                    is_guest=True
                )
                session.add(new_session)
                await session.commit()
        
        # Продолжаем обработку как для гостя
        current_user = {"id": None, "is_guest": True}
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
    
@router.get("/history/{session_id}", response_model=list[MessageInfoResponse])
@limiter.limit(Config.RATE_LIMITS["history"])
async def get_session_messages(
    request: Request,
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    session_id = ''
    # Гостевой доступ
    if current_user is None:
        guest_data = get_guest_session_id(request)
        if guest_data['question_count'] >= 10:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Guest limit exceeded. Please register to continue."
            )
        guest_data['question_count'] += 1
        
        session_id = guest_data['session_id']
        async with async_session() as session:
            # Проверяем/создаем сессию
            existing_session = await session.execute(
                select(SessionInfo).where(SessionInfo.session_id == session_id)
            )
            if not existing_session.scalars().first():
                new_session = SessionInfo(
                    session_id=session_id,
                    user_id=None,
                    name="Guest Session",
                    created_at=datetime.datetime.now(),
                    is_guest=True
                )
                session.add(new_session)
                await session.commit()
        
        # Продолжаем обработку как для гостя
        current_user = {"id": None, "is_guest": True}
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
        
@router.patch("/history/{session_id}/rename", response_model=SessionInfoResponse)
@limiter.limit(Config.RATE_LIMITS["history"])
async def rename_session(
    request: Request,
    session_id: str = Path(..., description="ID сессии для переименования"),
    rename_data: RenameSessionRequest = None,
    current_user: dict = Depends(get_current_user)
):
    session_id = ''
    # Гостевой доступ
    if current_user is None:
        guest_data = get_guest_session_id(request)
        if guest_data['question_count'] >= 10:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Guest limit exceeded. Please register to continue."
            )
        guest_data['question_count'] += 1
        
        session_id = guest_data['session_id']
        print("session_id", session_id)
        async with async_session() as session:
            # Проверяем/создаем сессию
            existing_session = await session.execute(
                select(SessionInfo).where(SessionInfo.session_id == session_id)
            )
            if not existing_session.scalars().first():
                new_session = SessionInfo(
                    session_id=session_id,
                    user_id=None,
                    name="Guest Session",
                    created_at=datetime.datetime.now(),
                    is_guest=True
                )
                session.add(new_session)
                await session.commit()
        
        # Продолжаем обработку как для гостя
        current_user = {"id": None, "is_guest": True}
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

