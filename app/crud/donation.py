from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """Класс для реализации уникальных методов модели Donation."""

    async def get_user_donation(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        """Получить список пожертвований текущего пользователя."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
