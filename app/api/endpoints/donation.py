from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    AllDonationsDBSchema,
    DonationCreateSchema,
    DonationDBSchema
)
from app.services.investment import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[AllDonationsDBSchema],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Список пожертвований'
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.read_all(session=session)


@router.post(
    '/',
    response_model=DonationDBSchema,
    response_model_exclude_none=True,
    summary='Создать пожертвование'
)
async def create_donation(
    donation_in: DonationCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(
        obj_in=donation_in, session=session, user=user
    )
    await investment(session=session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDBSchema],
    summary='Список пожертвований текущего пользователя'
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_user_donations(user=user, session=session)
