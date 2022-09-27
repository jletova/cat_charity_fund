from typing import Optional
from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models import User


# class CRUDDonation(CRUDBase):

#     async def get_donations_at_the_same_time(
#         self,
#         from_reserve: datetime,
#         to_reserve: datetime,
#         CharityProject_id: int,
#         session: AsyncSession,
#     ) -> Optional[list[Donation]]:

#         donations = await session.execute(
#             select(Donation).where(
#                 Donation.CharityProject_id == CharityProject_id,
#                 or_(
#                     between(
#                         from_reserve,
#                         Donation.from_reserve,
#                         Donation.to_reserve
#                     ),
#                     between(
#                         to_reserve,
#                         Donation.from_reserve,
#                         Donation.to_reserve
#                     ),
#                     and_(
#                         from_reserve <= Donation.from_reserve,
#                         to_reserve >= Donation.to_reserve
#                     )
#                 )
#             )
#         )
#         return donations.scalars().all()


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id,
            )
        )
        return donations.scalars().all()


donations_crud = CRUDDonation(Donation)
