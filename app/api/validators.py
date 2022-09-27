from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import projects_crud
from app.crud.donation import donations_crud
from app.models import CharityProject, Donation, User


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await projects_crud.get_project_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exist(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await projects_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Ошибка. Такого проекта нет'
        )
    return charity_project


# async def check_before_edit(
#         donation_id: int,
#         session: AsyncSession,
#         user: User,
# ) -> Donation:
#     donation = await donations_crud.get(
#         obj_id=donation_id, session=session
#     )
#     if donation.fully_invested:
#         raise HTTPException(status_code=400, detail='Нельзя изменить проинвестированный проект!')

#     if not donation:
#         raise HTTPException(status_code=404, detail='Не найдено!')
#     if donation.user_id and donation.user_id != user.id or not user.is_superuser:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить!'
#         )
#     return donation