# app/api/meeting_room.py
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectUpdate, CharityProjectDB
)

from app.api.validators import (
    check_charity_project_exists, check_name_duplicate,
    check_no_invested_funds, check_greater_than_invested_funds,
)
from app.schemas.charityproject import CharityProjectDB, CharityProjectResponse
# from app.crud.reservation import reservation_crud
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    # await check_name_duplicate(meeting_room.name, session)
    # Замените вызов функции на вызов метода.

    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectResponse],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    # Замените вызов функции на вызов метода.
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_greater_than_invested_funds(obj_in.full_amount,
                                                charity_project)

    # Замените вызов функции на вызов метода.
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    charity_project = await check_charity_project_exists(charity_project_id,
                                                   session)
    charity_project = await check_no_invested_funds(charity_project)
    # Замените вызов функции на вызов метода.
    charity_project = await charity_project_crud.remove(charity_project,
                                                  session)
    return charity_project



# @router.get(
#     '/{meeting_room_id}/reservations',
#     response_model=list[ReservationDB],
#     # Добавляем множество с полями, которые надо исключить из ответа.
#     response_model_exclude={'user_id'},
# )
# async def get_reservations_for_room(
#         meeting_room_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     await check_meeting_room_exists(meeting_room_id, session)
#     reservations = await reservation_crud.get_future_reservations_for_room(
#         room_id=meeting_room_id, session=session
#     )
#     return reservations