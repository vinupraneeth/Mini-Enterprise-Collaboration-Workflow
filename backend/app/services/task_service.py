from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user_model import User

from app.schemas.task_schema import (
    TaskCreate,
    TaskStatusUpdate,
    TaskUpdate,
    TaskAssign
)

from app.repositories.task_repository import (
    create_task,
    get_all_tasks,
    get_tasks_by_user,
    get_tasks_created_by_user,
    get_task_by_id,
    update_task_status,
    delete_task,
    update_task
)


def validate_assignment(
    db: Session,
    current_user,
    assigned_to: int
):

    assigned_user = db.query(User).filter(
        User.id == assigned_to
    ).first()

    if not assigned_user:

        raise HTTPException(
            status_code=404,
            detail="Assigned user not found"
        )

    current_role = (
        current_user.role.lower()
    )

    assigned_role = (
        assigned_user.role.lower()
    )

    if current_role == "manager":

        if assigned_role != "employee":

            raise HTTPException(
                status_code=403,
                detail=
                "Manager can assign only to employees"
            )

    return assigned_user


def create_new_task(
    db: Session,
    task: TaskCreate,
    current_user
):

    validate_assignment(
        db,
        current_user,
        task.assigned_to
    )

    task_data = task.model_dump()

    task_data["created_by"] = (
        current_user.id
    )

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

def fetch_task_by_id(
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
            task.created_by
            ==
            current_user.id
        )

    elif role == "employee":

        allowed = (
            task.assigned_to
            ==
            current_user.id
        )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail=
            "Not authorized to view this task"
        )

    return task


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
            task.created_by
            ==
            current_user.id
        )

    elif role == "employee":

        allowed = (
            task.assigned_to
            ==
            current_user.id
        )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail=
            "Not authorized to update this task"
        )

    return update_task_status(
        db,
        task,
        status_data.status
    )


def edit_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
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
            task.created_by
            ==
            current_user.id
        )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail=
            "Not authorized to update task"
        )

    validate_assignment(
        db,
        current_user,
        task_data.assigned_to
    )

    return update_task(
        db,
        task,
        task_data.model_dump()
    )


def assign_task(
    db: Session,
    task_id: int,
    assign_data: TaskAssign,
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

    allowed = role in [
        "admin",
        "manager"
    ]

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail=
            "Not authorized to assign task"
        )

    validate_assignment(
        db,
        current_user,
        assign_data.assigned_to
    )

    task.assigned_to = (
        assign_data.assigned_to
    )

    db.commit()

    db.refresh(task)

    return task


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
            task.created_by
            ==
            current_user.id
        )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail=
            "Not authorized to delete this task"
        )

    delete_task(
        db,
        task
    )

