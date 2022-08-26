from app.models import CharityProject, Donation, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from typing import List

from app.schemas.charityproject import CharityProjectDB
from app.models.charityproject import CharityProject



# async def check_no_invested_funds(
#         charity_project: CharityProject,
# ) -> CharityProject:
#     if charity_project.invested_amount > 0:
#         raise HTTPException(status_code=422,
#                             detail='В проекте есть инвестированные средства.')
#     return charity_project





async def get_opened_charity_project(
        session: AsyncSession,
) -> List[CharityProject]:
    charity_project = await session.execute(
        select(
            CharityProject
        ).where(
            CharityProject.fully_invested == False  # noqa
        ).order_by(
            CharityProject.create_date
        )
    )
    return charity_project.scalars().all()


async def invest_when_new_donation(
        donation: Donation,
        session: AsyncSession,
) -> Donation:
    charity_projects = await get_opened_charity_project(session)
    for project in charity_projects:
        project_delta = project.full_amount - project.invested_amount
        donation_balance = donation.full_amount - donation.invested_amount
        """Пожертвование меньше, чем нужно проекту или под расчёт"""
        if donation_balance <= project_delta:
            project.invested_amount += donation_balance
            donation.invested_amount += donation_balance
            donation.close_date = datetime.now()
            donation.fully_invested = True

            if donation_balance == project_delta:
                project.close_date = datetime.now()
                project.fully_invested = True
                session.add(project)
            session.add(donation)
            break
        else:
            """Пожертвование больше, чем нужно"""
            donation.invested_amount += project_delta
            project.invested_amount = project.full_amount
            project.close_date = datetime.now()
            project.fully_invested = True
            session.add(project)
    await session.commit()
    await session.refresh(donation)
    return donation






    #     charity_delta = project.full_amount - project.invested_amount
    #     donation_delta = dn.full_amount - dn.invested_amount
    #     if donation_delta == charity_delta:
    #         dn, cp = make_investment_when_donation_equal_charity(
    #             dn, cp, donation_delta
    #         )
    #         session.add(cp)
    #         break
    #     elif donation_delta > charity_delta:
    #         dn, cp = make_investment_when_donation_more_charity(
    #             dn, cp, charity_delta
    #         )
    #         session.add(cp)
    #     else:
    #         dn, cp = make_investment_when_donation_less_charity(
    #             dn, cp, donation_delta
    #         )
    #         session.add(cp)
    #         break
    # session.add(dn)
    # await session.commit()
    # await session.refresh(dn)
    # return dn