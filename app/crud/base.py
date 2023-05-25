from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    """Базовый класс для выполнения операций получения и создания объектов."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> Optional[ModelType]:
        """Получить объект модели по id."""
        obj = await session.execute(
            select(self.model).where(self.model.id == obj_id))
        return obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        """Получить список объектов модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            data: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> ModelType:
        """Создать объект модели и записать в БД."""
        new_obj_data = data.dict()
        if user is not None:
            new_obj_data['user_id'] = user.id
        new_obj = self.model(**new_obj_data)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    async def get_active_objs(
            self,
            session: AsyncSession
    ) -> Optional[ModelType]:
        """Получить список активных объектов модели."""
        active_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == false()).order_by(
                    self.model.id)
        )
        return active_objs.scalars().all()
