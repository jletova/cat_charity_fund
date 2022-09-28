from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation
from app.schemas.donation import DonationDB


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> list[DonationDB]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id,
            )
        )
        return donations.scalars().all()


donations_crud = CRUDDonation(Donation)
