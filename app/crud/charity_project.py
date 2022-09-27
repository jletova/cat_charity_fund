from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    # async def get_projects_to_invest(
    #         self,
    #         session: AsyncSession,
    # ) -> CharityProject:
    #     projects_to_invest = await session.execute(
    #         select(CharityProject).where(
    #             CharityProject.fully_invested == 0)
    #     )
    #     return projects_to_invest

    async def get_project_id_by_name(
            self,
            room_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == room_name
            )
        )
        return db_room_id.scalars().first()


projects_crud = CRUDCharityProject(CharityProject)
