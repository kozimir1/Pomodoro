

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models import Tasks
from schema.task import TaskCreateSchema


class TaskRepository:

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_tasks(self) -> list[Tasks]:
        print(self.db_session,11)
        async with self.db_session as session:
            task = (await session.execute(select(Tasks))).scalars().all()
            return task

    async def get_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            task = (await session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
            return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(name=task.name,
                           pomodoro_count=task.pomodoro_count,
                           category_id=task.category_id,
                           user_id=user_id)
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            return task_model.id

    async def update_task_name(self, task_id: int, name: str) -> Tasks | None:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task_id)

    async def delete_task(self, task_id: int) -> None:
        async with self.db_session as session:
            await session.execute(delete(Tasks).where(Tasks.id == task_id))
            await session.commit()

    async def get_user_tasks(self, task_id, user_id) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

