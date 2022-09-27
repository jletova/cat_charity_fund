from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.charity_project import QRKotBaseModel


async def invest(
    project: QRKotBaseModel,
    in_obj_data: dict,
    session: AsyncSession,
) -> dict:
    data_to_update = {}
    need_amount = project.full_amount - project.invested_amount
    donate = in_obj_data['full_amount'] - in_obj_data.get('invested_amount', 0)
    if need_amount > donate:
        data_to_update['invested_amount'] = project.invested_amount + donate
        in_obj_data['invested_amount'] = in_obj_data['full_amount']
        in_obj_data['fully_invested'] = True
        in_obj_data['close_date'] = datetime.now()
    else:
        in_obj_data['invested_amount'] = in_obj_data.get('invested_amount', 0) + need_amount
        data_to_update['fully_invested'] = True
        data_to_update['close_date'] = datetime.now()
        data_to_update['invested_amount'] = project.full_amount

    for field in data_to_update:
        setattr(project, field, data_to_update[field])
    session.add(project)
    return in_obj_data