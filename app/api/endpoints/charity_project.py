from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_before_delete,
    check_charity_project_before_update,
    check_charity_project_name_duplilcate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreateSchema,
    CharityProjectDBSchema,
    CharityProjectUpdateSchema
)
from app.services.investment import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDBSchema],
    response_model_exclude_none=True,
    summary='Список всех проектов'
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.read_all(session=session)


@router.post(
    '/',
    response_model=CharityProjectDBSchema,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создать проект'
)
async def create_charity_project(
    charity_project: CharityProjectCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    await check_charity_project_name_duplilcate(
        charity_project_name=charity_project.name,
        session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project, session=session
    )
    await investment(session=session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDBSchema,
    dependencies=[Depends(current_superuser)],
    summary='Удалить проект'
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_before_delete(
        charity_project_id=project_id, session=session
    )
    deleted_charity_project = await charity_project_crud.delete(
        db_obj=charity_project, session=session
    )
    return deleted_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDBSchema,
    dependencies=[Depends(current_superuser)],
    summary='Редактировать проект'
)
async def update_charity_project(
    project_id: int,
    charity_project_in: CharityProjectUpdateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project_db = await check_charity_project_before_update(
        charity_project_id=project_id,
        session=session,
        charity_project_in=charity_project_in
    )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project_db, obj_in=charity_project_in, session=session
    )
    return charity_project
