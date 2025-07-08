from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from api.config import settings
from contextlib import asynccontextmanager

DATABASE_URL = f"{settings.DATABASE_URL}{settings.DATABASE_NAME}"

Base = declarative_base()

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование запросов (можно отключить в продакшене)
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,  # Пересоздавать соединения каждые час
)

# Настройка фабрики сессий
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Не истекать после коммита
    autoflush=False,
    autocommit=False,
)

@asynccontextmanager
async def get_session():
    """Асинхронный контекстный менеджер для работы с сессиями БД."""
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()