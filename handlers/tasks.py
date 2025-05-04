from fastapi import APIRouter, status, Depends
from typing import Annotated

from dependecy import get_tasks_repository, get_cache_repository, get_service_repository,get_request_user_id
from repository import TaskRepository, CacheRepository
from schema.task import TaskSchema
from servise import TaskService

from fixtures import tasks as fixture_tasks


router=APIRouter(prefix='/task', tags=['task'])


@router.get('/all',
            response_model=list[TaskSchema]
            )
async def get_task(task_servise: Annotated[TaskService, Depends(get_service_repository)]):
    return task_servise.get_tasks()


@router.post('/',
             response_model=TaskSchema
             )
async def create_tasks(
        task: TaskSchema,
        task_repositiry: Annotated[TaskRepository,Depends(get_tasks_repository)],
        user_id: int = Depends(get_request_user_id)):
    task_id = task_repositiry.create_task(task)
    task.id=task_id
    return task

@router.patch('/{task_id}',
              response_model=TaskSchema)
async def update_tasks(task_id :int,
                       name: str,
                       task_repositiry: Annotated[TaskRepository,Depends(get_tasks_repository)]):
    return task_repositiry.update_task_name(task_id, name)

@router.delete('/{task_id}',
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_tasks(task_id: int,
                       task_repositiry: Annotated[TaskRepository,Depends(get_tasks_repository)]):
    task_repositiry.delete_task(task_id)
    return {'message': f'Deleted {task_id}'}




