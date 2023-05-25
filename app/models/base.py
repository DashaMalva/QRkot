from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.sql import false

from app.core.db import Base


class BaseCharityModel(Base):
    """Абстрактная модель для моделей Пожертвования и Благотв.проекта."""
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=false())
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
