from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from MyService.core.db import get_db
from MyService.core.entities.tasks import TaskCreate, TaskUpdate
from MyService.core.models import Task
from . import crud

router = APIRouter(tags=["Tasks"])


@router.get("/", summary="Получает список всех задач",
            response_model=list[Task], status_code=status.HTTP_200_OK)
async def get_tasks(session: AsyncSession = Depends(get_db)) -> list[Task]:
    tasks = await crud.get_tasks(session)
    return tasks


@router.post("/", summary="Создает задачу", response_model=Task,
             status_code=status.HTTP_201_CREATED)
async def create_task(
        task_data: TaskCreate,
        session: AsyncSession = Depends(get_db)
):
    task = await crud.create_task(session=session, task_data=task_data)
    return task


@router.get("/{task_uuid}/", summary="Получает задачу по uuid", response_model=Task)
async def get_task(
        task_uuid: str,
        session: AsyncSession = Depends(get_db)
):
    task = await crud.get_task(session, task_uuid)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_uuid}/", summary="Обновляет задачу по uuid", response_model=Task)
async def update_task(
        task_uuid: str,
        task_update: TaskUpdate,
        session: AsyncSession = Depends(get_db)
):
    update_data = task_update.model_dump(exclude_unset=True)
    updated_task = await crud.update_task(session=session,
                                          task_uuid=task_uuid,
                                          update_data=update_data)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_uuid}/", summary="Удаляет задачу по uuid",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_uuid: str,
        session: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_task(session=session, task_uuid=task_uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
