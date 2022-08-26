from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User  # noqa
from app.schemas.donation import (  # noqa
    DonationCreate, DonationDB  # noqa
)  # noqa
from app.services.donation_investment import (  # noqa
    invest_when_new_donation)  # noqa
  # noqa
router = APIRouter()


@router.post('/',
             response_model=DonationDB,
             response_model_exclude_none=True,
             response_model_include={
                 'id', 'comment', 'full_amount', 'create_date'
             }
             )
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    await invest_when_new_donation(new_donation, session)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations  # noqa


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    response_model_include={
        'comment', 'create_date', 'full_amount', 'id'
    }
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(session=session,
                                                user=user)

    return donations  # noqa
