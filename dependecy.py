from fastapi import Depends, Request, security, Security, HTTPException
from typing import Annotated

from database import get_db_session
from exception import TokenExpired, TokenNotCorrect
from repository import TaskRepository, CacheRepository, UserRepository
from cache import get_redis_connection
from servise import TaskService, UserService, AuthService
from settings import Settings


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session=db_session)


def get_cache_repository() -> CacheRepository:
    redis = get_redis_connection()
    return CacheRepository(redis)


def get_task_service(
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


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())


def get_user_service(user_repository: UserRepository = Depends(get_user_repository),
                     auth_service: AuthService = Depends(get_auth_service)) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
                        auth_service: AuthService = Depends(get_auth_service)) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail)
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail)
    return user_id
