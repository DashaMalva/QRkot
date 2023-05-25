from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseCharityModel


class Donation(BaseCharityModel):
    """Модель Пожертвования.

    Fields:
    user_id: str, auto_add
        id пользователя, сделавшего пожертвование
    comment: str, optional
        комментарий к пожертвованию
    full_amount: int, required
        сумма пожертвования
    invested_amount: int, auto_add
        сумма из пожертвования, которая распределена по проектам (default = 0)
    fully_invested: bool, auto_add
        флаг, указывающий все ли пожертвование распределено (default = False)
    create_date: datetime, auto_add
        дата поступления пожертвования
    close_date: datetime, optional, auto_add
        дата полного распределения пожертвования (default = None)
    id: int, primary key
        идентификатор проекта, первичный ключ
    """
    user_id = Column(Integer, ForeignKey('user.id',
                                         name='fk_donation_user_id_user'))
    comment = Column(Text)
