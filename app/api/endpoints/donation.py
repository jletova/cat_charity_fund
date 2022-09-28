from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import projects_crud
from app.crud.donation import donations_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.base import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested', 'close_date'
    },
    dependencies=[Depends(current_user)]
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donations_crud.create(donation, session, user)

    projects = await projects_crud.get_by_attribute('fully_invested', 0, session)
    if projects:
        new_donation = await invest(new_donation, projects, session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """All donations. Only for superusers."""
    donations = await donations_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested', 'close_date'
    },
    dependencies=[Depends(current_user)]
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """User's donation."""
    donations = await donations_crud.get_by_user(
        session=session, user=user
    )
    return donations
