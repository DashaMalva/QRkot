from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.schemas.base import BaseDB


class CharityProjectBase(BaseModel):
    """Базовая pydantic-схема благотвор.проекта."""
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    """Pydantic-схема для обновления благотвор.проекта."""

    class Config:
        schema_extra = {
            'example': {
                'name': 'Toys for cats',
                'description': 'Cats need to have fun',
                'full_amount': 10000
            }
        }

    @validator('name', 'description', 'full_amount')
    def fields_cannot_be_null(cls, value):
        """Проверяет, что при изменении обязательных полей объекта,
        их значения не стали пустыми."""
        if value is None:
            raise ValueError('Поле не может быть пустым!')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    """Pydantic-схема для создания благотвор.проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectBase, BaseDB):
    """Pydantic-схема для вывода информации о благотвор.проекте."""
    pass
