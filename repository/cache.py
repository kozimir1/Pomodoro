from redis import asyncio as Redis
import json

from schema.task import TaskSchema


class CacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskSchema]:
        async with self.redis as redis:
            tasks_json = await redis.lrange('tasks', 0, -1)
            return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]

    async def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = (task.model_dump_json() for task in tasks)
        async with self.redis as redis:
            await redis.rpush('tasks', *tasks_json)
