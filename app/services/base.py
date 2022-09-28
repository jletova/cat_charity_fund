from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

# from app.core.db import get_async_session
from app.schemas.charity_project import QRKotBaseModel


async def invest(
    new_object: QRKotBaseModel,
    projects_to_invest: list[QRKotBaseModel],
    session: AsyncSession,
) -> QRKotBaseModel:
    for project_to_invest in projects_to_invest:
        project_to_invest = project_to_invest[0]
        # print('___ДО___', jsonable_encoder(new_object), jsonable_encoder(project_to_invest))

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
        # print('__ПОСЛЕ__', jsonable_encoder(new_object), jsonable_encoder(project_to_invest))

        if new_object.fully_invested:
            break
    # await session.commit()
    # await session.refresh(new_object)
    return new_object