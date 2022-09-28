from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import projects_crud
from app.schemas.charity_project import CharityProjectDB


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
) -> Optional[CharityProjectDB]:
    charity_project = await projects_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Ошибка. Такого проекта нет'
        )
    return charity_project
