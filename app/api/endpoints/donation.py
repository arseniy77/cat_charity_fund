from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_name_duplicate,
    check_no_invested_funds, check_greater_than_invested_funds,
)
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB
)
from app.core.user import current_user
from app.models import User
from app.core.user import current_superuser
from app.services.investment import (
    get_opened_charity_project, invest_when_new_donation)

router = APIRouter()


@router.post('/',
             response_model=DonationDB,
             response_model_exclude_none=True,)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        # Получаем текущего пользователя и сохраняем в переменную user.
        user: User = Depends(current_user),
):
    # await check_charity_project_exists(
    #     donation.meetingroom_id, session
    # )
    # await check_reservation_intersections(
    #     **reservation.dict(), session=session
    # )
    new_donation = await donation_crud.create(
        # Передаём объект пользователя в метод создания объекта бронирования.
        donation, session, user
    )
    await invest_when_new_donation(new_donation, session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    # Замените вызов функции на вызов метода.
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(session=session,
                                                user=user)

    print(donations)

    test = await get_opened_charity_project(session)
    print(test)
    for _ in test:
        print(_.name)



    return donations