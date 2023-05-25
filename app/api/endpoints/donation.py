from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.schemas import DonationCreate, DonationFullDB, DonationShortDB
from app.services.invest import invest
from app.models import User


router = APIRouter()


@router.get('/',
            response_model=list[DonationFullDB],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Получение списка всех пожертвований. Только для суперюзеров."""
    return await donation_crud.get_multi(session=session)


@router.post('/',
             response_model=DonationShortDB,
             response_model_exclude_none=True)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создание пожертвования. Только для авторизованных пользователей."""
    new_donation = await donation_crud.create(
        data=donation, session=session, user=user)
    active_projects = await charity_project_crud.get_active_objs(session)
    if active_projects:
        await invest(new_donation, active_projects, session)
    return new_donation


@router.get('/my',
            response_model=list[DonationShortDB],
            response_model_exclude_none=True)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получение списка своих пожертвований.
    Только для авторизованных пользователей.
    """
    return await donation_crud.get_user_donation(
        session=session, user=user)
