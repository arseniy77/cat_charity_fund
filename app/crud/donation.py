# app/crud/reservation.py
from app.crud.base import CRUDBase
from app.models import Donation, User
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, between, or_, select
from typing import Optional


class CRUDDonation(CRUDBase):

    # async def get_reservations_at_the_same_time(
    #         self,
    #         *,
    #         from_reserve: datetime,
    #         to_reserve: datetime,
    #         meetingroom_id: int,
    #         reservation_id: Optional[int] = None,
    #         session: AsyncSession,
    # ) -> list[Reservation]:
    #     select_stmt = select(Reservation).where(
    #         Reservation.meetingroom_id == meetingroom_id,
    #         and_(
    #             from_reserve <= Reservation.to_reserve,
    #             to_reserve >= Reservation.from_reserve
    #         )
    #     )
    #     # Если передан id бронирования...
    #     if reservation_id is not None:
    #         # ... то к выражению нужно добавить новое условие.
    #         select_stmt = select_stmt.where(
    #             # id искомых объектов не равны id обновляемого объекта.
    #             Reservation.id != reservation_id
    #         )
    #     reservations = await session.execute(select_stmt)
    #     reservations = reservations.scalars().all()
    #     return reservations

    # async def get_future_reservations_for_room(
    #         self,
    #         room_id: int,
    #         session: AsyncSession,
    # ):
    #     reservations = await session.execute(
    #         # Получить все объекты Reservation.
    #         select(Reservation).where(
    #             # Где внешний ключ meetingroom_id
    #             # равен id запрашиваемой переговорки.
    #             Reservation.meetingroom_id == room_id,
    #             # А время конца бронирования больше текущего времени.
    #             Reservation.to_reserve > datetime.now()
    #         )
    #     )
    #     reservations = reservations.scalars().all()
    #     return reservations

    # Новый метод:
    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


        # Создаём объекта класса CRUDReservation.
donation_crud = CRUDDonation(Donation)
