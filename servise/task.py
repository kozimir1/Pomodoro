from exception import TaskNotFound
from repository import TaskRepository, CacheRepository
from schema.task import TaskSchema, TaskCreateSchema
from dataclasses import dataclass


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheRepository

    async def get_tasks(self) -> list[TaskSchema]:
        if tasks := await self.task_cache.get_tasks():
            return tasks
        else:
            tasks = await self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id)
        return TaskSchema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_user_tasks(task_id=task_id,
                                                   user_id=user_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_task_name(task_id=task_id,
                                                     name=name)
        return TaskSchema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_tasks(task_id=task_id,
                                                         user_id=user_id)
        if not task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id)
