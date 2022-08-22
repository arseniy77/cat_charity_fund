# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject, Donation, User

# from app.crud.reservation import reservation_crud


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(project_name,
                                                          session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id,
                                               session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return charity_project


# async def check_reservation_intersections(**kwargs) -> None:
#     reservations = await reservation_crud.get_reservations_at_the_same_time(
#         **kwargs
#     )
#     if reservations:
#         raise HTTPException(
#             status_code=422,
#             detail=str(reservations)
#         )
#
#
# async def check_reservation_before_edit(
#         reservation_id: int,
#         session: AsyncSession,
#         # Новый параметр корутины.
#         user: User,
# ) -> Reservation:
#     reservation = await reservation_crud.get(
#         obj_id=reservation_id, session=session
#     )
#     if not reservation:
#         raise HTTPException(status_code=404, detail='Бронь не найдена!')
#     # Новая проверка и вызов исключения.
#     if reservation.user_id != user.id and not user.is_superuser:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить чужую бронь!'
#         )
#     return reservation