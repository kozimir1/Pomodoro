from redis import Redis
import json

from schema.task import TaskSchema


class CacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis as redis:
            tasks_json = redis.lrange('tasks', 0, -1)
            return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = (task.model_dump_json() for task in tasks)
        with self.redis as redis:
            redis.rpush('tasks', *tasks_json)

