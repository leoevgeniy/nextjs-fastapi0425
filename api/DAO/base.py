from typing import List, Optional, TypeVar, Type
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from datetime import datetime
from contextlib import asynccontextmanager

from api.database.database import async_session
from api.models.product import Promos
from api.schema.schema import Color, ProductIndex, Size

T = TypeVar('T', bound='BaseDAO')

class BaseDAO:
    model = None
    
    @classmethod
    @asynccontextmanager
    async def _get_session(cls):
        """Внутренний метод для получения сессии."""
        async with async_session() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
    
    @classmethod
    async def find_one_or_none(cls: Type[T], **kwargs) -> Optional[T]:
        async with cls._get_session() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls: Type[T], **kwargs) -> List[T]:
        async with cls._get_session() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def add(cls: Type[T], **data) -> T:
        async with cls._get_session() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            return instance
    
    @classmethod
    async def update_by_id(cls: Type[T], id: int, **updating_data) -> Optional[T]:
        async with cls._get_session() as session:
            instance = await cls.find_one_or_none(id=id)
            if instance:
                for key, value in updating_data.items():
                    setattr(instance, key, value)
                await session.commit()
                return instance
            return None
    
    @classmethod
    async def get_paginated(
        cls: Type[T], 
        offset: int = 0, 
        limit: int = 12, 
        **kwargs
    ) -> List[T]:
        async with cls._get_session() as session:
            query = select(cls.model).filter_by(**kwargs).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def get_count(cls: Type[T], **kwargs) -> int:
        async with cls._get_session() as session:
            query = select(func.count()).select_from(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one()
    
    # Специфичные методы для работы с промо-акциями
    @classmethod
    async def get_active_promos(cls) -> List[Promos]:
        async with cls._get_session() as session:
            query = select(Promos).where(
                Promos.endDate > datetime.now(),
                Promos.startDate <= datetime.now()
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def get_products_for_promo(cls: Type[T], promo_id: int) -> Optional[List[T]]:
        async with cls._get_session() as session:
            promo = await session.get(Promos, promo_id)
            if not promo or not promo.products:
                return None
                
            product_ids = [pid.strip() for pid in promo.products.split(',')]
            query = select(cls.model).where(
                cls.model.prodID.in_(product_ids),
                cls.model.stock > 0
            ).group_by(cls.model.prodID)
            
            result = await session.execute(query)
            return result.scalars().all()