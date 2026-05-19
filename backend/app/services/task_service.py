from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schemas.task_schema import (
    TaskCreate,
    TaskStatusUpdate
)

from app.repositories.task_repository import (
    create_task,
    get_all_tasks,
    get_tasks_by_user,
    get_tasks_created_by_user,
    get_task_by_id,
    update_task_status,
    delete_task
)

def create_new_task(
    db: Session,
    task: TaskCreate,
    current_user
):

    task_data = task.model_dump()

    task_data["created_by"] = current_user.id

    return create_task(
        db,
        task_data
    )

def fetch_tasks(
    db: Session,
    current_user
):

    role = current_user.role.lower()

    if role == "admin":

        return get_all_tasks(db)

    if role == "manager":

        return get_tasks_created_by_user(
            db,
            current_user.id
        )

    return get_tasks_by_user(
        db,
        current_user.id
    )


def change_task_status(
    db: Session,
    task_id: int,
    status_data: TaskStatusUpdate,
    current_user
):

    task = get_task_by_id(
        db,
        task_id
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    role = current_user.role.lower()

    allowed = False

    if role == "admin":

        allowed = True

    elif role == "manager":

        allowed = (
            task.created_by == current_user.id
        )

    elif role == "employee":

        allowed = (
            task.assigned_to == current_user.id
        )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this task"
        )

    return update_task_status(
        db,
        task,
        status_data.status
    )


def remove_task(
    db: Session,
    task_id: int,
    current_user
):

    task = get_task_by_id(
        db,
        task_id
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    role = current_user.role.lower()

    allowed = False

    if role == "admin":

        allowed = True

    elif role == "manager":

        allowed = (
            task.created_by == current_user.id
        )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this task"
        )

    delete_task(
        db,
        task
    )