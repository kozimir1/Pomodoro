from repository import TaskRepository, CacheRepository
from schema.task import TaskSchema
from dataclasses import dataclass


@dataclass
class TaskServise:
    task_repository: TaskRepository
    task_cache: CacheRepository

    def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema
