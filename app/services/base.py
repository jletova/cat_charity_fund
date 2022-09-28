from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import QRKotBaseModel


async def invest(
    new_object: QRKotBaseModel,
    projects_to_invest: list[QRKotBaseModel],
    session: AsyncSession,
) -> QRKotBaseModel:
    """Investment process."""
    for project_to_invest in projects_to_invest:
        # project_to_invest = project_to_invest[0]

        need_amount = project_to_invest.full_amount - project_to_invest.invested_amount
        if new_object.full_amount > need_amount:
            new_object.invested_amount = new_object.invested_amount + need_amount
            project_to_invest.invested_amount = project_to_invest.full_amount
        elif new_object.full_amount < need_amount:
            project_to_invest.invested_amount = project_to_invest.invested_amount + new_object.full_amount
            new_object.invested_amount = new_object.full_amount
        elif new_object.full_amount == need_amount:
            new_object.invested_amount = new_object.full_amount
            project_to_invest.invested_amount = project_to_invest.full_amount

        if new_object.invested_amount == new_object.full_amount:
            new_object.fully_invested = True
            new_object.close_date = datetime.now()
        if project_to_invest.invested_amount == project_to_invest.full_amount:
            project_to_invest.fully_invested = True
            project_to_invest.close_date = datetime.now()

        session.add(project_to_invest)
        session.add(new_object)

        if new_object.fully_invested:
            break
    await session.commit()
    await session.refresh(new_object)
    return new_object