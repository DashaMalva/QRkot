from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def close_obj(
        obj: Union[CharityProject, Donation],
        obj_close_date: datetime
) -> None:
    """Меняет статус объекта Пожертвование / Благотв.проект на закрытый."""
    obj.fully_invested = True
    obj.close_date = obj_close_date
    obj.invested_amount = obj.full_amount


async def invest(
        obj_to_invest: Union[CharityProject, Donation],
        investments: Union[list[CharityProject], list[Donation]],
        session: AsyncSession
) -> None:
    """Процесс инвестирования.
    В случае, если obj_to_invest является пожертвованием (Donation),
    а investments - незакрытыми благотв.проектами (list[CharityProject]),
    процесс инвестирования представляет собой распределение суммы пожертвования
    между незакрытыми проектами.
    В случае, если obj_to_invest является благотвор.проектом (CharityProject),
    а investments - нераспределенными пожертвованиями (list[Donation]),
    процесс инвестирования представляет собой добавление в проект сумм
    нераспределенных пожертвований.
    В процессе инвестирования объекты, средства которых были распределены,
    будут закрыты. Изменения сохраняются в БД.
    """
    full_amount: int = obj_to_invest.full_amount
    close_date = datetime.now()

    for investment in investments:
        current_amount: int = full_amount - (
            investment.full_amount - investment.invested_amount)

        if current_amount > 0:
            close_obj(investment, close_date)
            obj_to_invest.invested_amount += full_amount - current_amount
            full_amount = current_amount
        elif current_amount < 0:
            close_obj(obj_to_invest, close_date)
            investment.invested_amount += full_amount
        else:
            close_obj(investment, close_date)
            close_obj(obj_to_invest, close_date)

        session.add(investment)

        if current_amount <= 0:
            break

    session.add(obj_to_invest)
    await session.commit()
    await session.refresh(obj_to_invest)
