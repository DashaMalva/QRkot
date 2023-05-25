from sqlalchemy import Column, String, Text

from app.models.base import BaseCharityModel


class CharityProject(BaseCharityModel):
    """Модель Благотворительного проекта.

    Fields:
    name: str, unique, required
        название проекта
    description: str, required
        описание проекта
    full_amount: int, required
        требуемая сумма
    invested_amount: int, auto_add
        внесенная сумма (default = 0)
    fully_invested: bool, auto_add
        флаг, указывающий закрыт ли проект (default = False)
    create_date: datetime, auto_add
        дата создания проекта
    close_date: datetime, auto_add
        дата закрытия проекта (default = None)
    id: int, primary key
        идентификатор проекта, первичный ключ
    """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return self.name
