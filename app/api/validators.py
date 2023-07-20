from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdateSchema


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.read_single(
        obj_id=charity_project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проекта с указанным id не существует!'
        )
    return charity_project


async def check_charity_project_name_duplilcate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_before_delete(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=('В проект были внесены средства, не подлежит удалению!')
        )
    return charity_project


async def check_charity_project_before_update(
    charity_project_id: int,
    charity_project_in: CharityProjectUpdateSchema,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    full_amount_update_value = charity_project_in.full_amount
    if (full_amount_update_value and
       charity_project.invested_amount > full_amount_update_value):
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую cумму меньше уже вложенной'
        )
    name_update_value = charity_project_in.name
    await check_charity_project_name_duplilcate(
        charity_project_name=name_update_value, session=session
    )
    return charity_project
