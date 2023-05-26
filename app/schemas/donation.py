from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import BaseDB


class DonationCreate(BaseModel):
    """Pydantic-схема для создания пожертвования."""
    full_amount: PositiveInt = Field(example=10000)
    comment: Optional[str]


class DonationFullDB(DonationCreate, BaseDB):
    """Pydantic-схема для вывода полной информации о пожертвовании."""
    user_id: int


class DonationShortDB(DonationCreate):
    """Pydantic-схема для вывода короткой информации о пожертвовании."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
