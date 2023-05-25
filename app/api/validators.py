from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_charity_project_before_edit(
        charity_project: CharityProject,
        update_data: CharityProjectUpdate
) -> None:
    """Проверяет, инвестиции проекта перед его редактированием."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    if (update_data.full_amount and
       update_data.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=422,
            detail='Требуемая сумма не может быть меньше уже внесенной!'
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверяет, что проект с переданным id существует."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_is_not_invested(
        charity_project: CharityProject
) -> None:
    """Проверяет, внесены ли в проект пожертвования."""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_charity_project_name_uniqueness(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверяет уникальность имени проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name=project_name, session=session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )
