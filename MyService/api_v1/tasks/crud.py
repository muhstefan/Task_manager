from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from MyService.core.entities.tasks import TaskCreate
from MyService.core.models import Task


async def get_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task).order_by(Task.status)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_task(session: AsyncSession, task_uuid: str) -> Optional[Task]:
    task = await session.get(Task, task_uuid)
    return task


async def create_task(session: AsyncSession, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(session: AsyncSession, task_uuid: str, update_data: dict) -> Optional[Task]:
    task = await get_task(session, task_uuid)
    if not task:
        return None
    for name, value in update_data.items():
        setattr(task, name, value)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_uuid: str) -> bool:
    task = await get_task(session, task_uuid)
    if not task:
        return False
    await session.delete(task)
    await session.commit()
    return True
