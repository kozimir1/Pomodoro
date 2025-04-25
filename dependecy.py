from fastapi import Depends
from typing import Annotated

from database import get_db_session
from repository import TaskRepository, CacheRepository
from cache import get_redis_connection
from servise import TaskServise


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_cache_repository() -> CacheRepository:
    redis = get_redis_connection()
    return CacheRepository(redis)


def get_servise_repository(
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
        task_cache: Annotated[CacheRepository, Depends(get_cache_repository)]
        ) -> TaskServise:
    return TaskServise(
        task_repository=task_repository,
        task_cache=task_cache
    )
