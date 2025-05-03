from fastapi import Depends
from typing import Annotated

from database import get_db_session
from repository import TaskRepository, CacheRepository, UserRepository
from cache import get_redis_connection
from servise import TaskService, UserService, AuthService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session=db_session)


def get_cache_repository() -> CacheRepository:
    redis = get_redis_connection()
    return CacheRepository(redis)


def get_service_repository(
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
        task_cache: Annotated[CacheRepository, Depends(get_cache_repository)]
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


def get_user_repository() -> UserRepository:
    db_session = get_db_session()
    return UserRepository(db_session=db_session)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository)
