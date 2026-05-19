from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.schemas.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate
)

from app.services.task_service import (
    create_new_task,
    fetch_tasks,
    change_task_status,
    remove_task
)

from app.core.dependencies import (
    get_current_user,
    require_manager_or_admin
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201
)
def create_task_api(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_manager_or_admin
    )
):

    return create_new_task(
        db,
        task,
        current_user
    )


@router.get(
    "/",
    response_model=list[TaskResponse]
)
def get_tasks_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return fetch_tasks(
        db,
        current_user
    )


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse
)
def update_task_status_api(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return change_task_status(
        db,
        task_id,
        status_data,
        current_user
    )


@router.delete(
    "/{task_id}",
    status_code=204
)
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    remove_task(
        db,
        task_id,
        current_user
    )