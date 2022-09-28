from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.user import current_superuser

from app.crud.charity_project import projects_crud
from app.crud.donation import donations_crud

from app.core.db import get_async_session
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.api.validators import check_name_duplicate, check_project_exist
from app.services.base import invest


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Only for superuser."""
    await check_name_duplicate(charity_project.name, session)
    new_object = await projects_crud.create(charity_project, session)
    objects_to_invest = await donations_crud.get_by_attribute('fully_invested', 0, session)
    if objects_to_invest:
        new_object = await invest(new_object, objects_to_invest, session)
    await session.commit()
    await session.refresh(new_object)
    return new_object


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_exist(
        project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя менять закрытый проект.'
        )
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.name is None or obj_in.name == '':
        obj_in.name = charity_project.name
    if obj_in.full_amount and (obj_in.full_amount < charity_project.invested_amount or obj_in.full_amount is None):
        raise HTTPException(
            status_code=404,
            detail='Сумма должна быть больше уже внесенной.'
        )
    if obj_in.description and obj_in.description is None:
        raise HTTPException(
            status_code=400,
            detail='Описание не может быть пустым.'
        )
    charity_project = await projects_crud.update(
        charity_project, obj_in, session
    )
    donations = await donations_crud.get_by_attribute('fully_invested', 0, session)
    if donations:
        charity_project = await invest(charity_project, donations, session)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    charity_project = await check_project_exist(
        project_id, session
    )
    if charity_project.invested_amount or charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    charity_project = await projects_crud.remove(charity_project, session)
    return charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
) -> list[CharityProjectDB]:
    all_projects = await projects_crud.get_multi(session)
    if all_projects is None:
        raise HTTPException(
            status_code=404,
            detail='Нет проектов для поддержки котиков',
        )
    return all_projects
