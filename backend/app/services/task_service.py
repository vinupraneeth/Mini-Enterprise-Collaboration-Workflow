from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.task_model import Task

from app.models.task_history_model import (
    TaskHistory
)

from app.models.approval_model import (
    Approval
)

from app.models.user_model import (
    User
)

from sqlalchemy import desc

from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate
)

from app.repositories.task_repository import (

    create_task,

    get_all_tasks,

    get_task_by_id,

    update_task,

    delete_task
)


VALID_TRANSITIONS = {

    "todo": [
        "in_progress"
    ],

    "in_progress": [
        "review"
    ],

    "review": [
        "done"
    ],

    "done": []
}


def validate_assignment(

    db: Session,

    assigned_to: int,

    current_user
):

    assigned_user = db.query(User).filter(
        User.id == assigned_to
    ).first()

    if not assigned_user:

        raise HTTPException(

            status_code=404,

            detail="Assigned user not found"
        )

    if (

        current_user.role == "manager"

        and

        assigned_user.role != "employee"
    ):

        raise HTTPException(

            status_code=403,

            detail="Managers can assign only to employees"
        )

    return assigned_user


def create_new_task(

    db: Session,

    task_data: TaskCreate,

    current_user
):

    if current_user.role not in [

        "admin",

        "manager"
    ]:

        raise HTTPException(

            status_code=403,

            detail=
            "Not authorized"
        )

    validate_assignment(
        db,
        task_data.assigned_to,
        current_user
    )

    task = Task(

        title=task_data.title,

        description=
            task_data.description,

        priority=
            task_data.priority,

        due_date=
            task_data.due_date,

        assigned_to=
            task_data.assigned_to,

        created_by=
            current_user.id,

        status="todo"
    )

    return create_task(

        db,

        task,

        current_user.id
    )


def fetch_tasks(

    db: Session,

    current_user
):

    tasks = get_all_tasks(db)

    if current_user.role == "admin":

        filtered_tasks = tasks

    elif current_user.role == "manager":

        filtered_tasks = [

            task

            for task in tasks

            if (

                task.created_by
                == current_user.id

                or

                task.assigned_to
                == current_user.id
            )
        ]

    elif current_user.role == "employee":

        filtered_tasks = [

            task

            for task in tasks

            if (
                task.assigned_to
                == current_user.id
            )
        ]

    else:

        filtered_tasks = []


    # APPROVAL FEEDBACK

    for task in filtered_tasks:

        latest_approval = db.query(
            Approval
        ).filter(

            Approval.task_id == task.id

        ).order_by(

            desc(Approval.id)

        ).first()

        if latest_approval:

            task.approval_status = (
                latest_approval.status
            )

            task.approval_remarks = (
                latest_approval.remarks
            )

        else:

            task.approval_status = None

            task.approval_remarks = None

    return filtered_tasks


def fetch_task_by_id(
    db: Session,
    task_id: int,
    current_user
):
    task = get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if current_user.role == "employee" and task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if current_user.role == "manager":
        if task.created_by != current_user.id and task.assigned_to != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

    return task


def assign_task(

    db: Session,

    task_id: int,

    assigned_to: int,

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

    if current_user.role not in [

        "admin",

        "manager"
    ]:

        raise HTTPException(

            status_code=403,

            detail=
            "Not authorized"
        )

    if current_user.role == "manager" and task.created_by != current_user.id:

        raise HTTPException(

            status_code=403,

            detail="Managers can assign only their own tasks"
        )

    validate_assignment(
        db,
        assigned_to.assigned_to,
        current_user
    )

    task.assigned_to = (
        assigned_to.assigned_to
    )

    task.updated_by = current_user.id

    db.commit()

    db.refresh(task)

    return task


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

    if current_user.role not in [

        "admin",

        "manager"
    ]:

        raise HTTPException(

            status_code=403,

            detail=
            "Not authorized"
        )

    if current_user.role == "manager" and task.created_by != current_user.id:

        raise HTTPException(

            status_code=403,

            detail="Managers can update only their own tasks"
        )

    validate_assignment(
        db,
        task_data.assigned_to,
        current_user
    )

    return update_task(
        db,
        task,
        task_data,
        current_user.id
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

    if current_user.role not in [

        "admin",

        "manager"
    ]:

        raise HTTPException(

            status_code=403,

            detail=
            "Not authorized"
        )

    if current_user.role == "manager" and task.created_by != current_user.id:

        raise HTTPException(

            status_code=403,

            detail="Managers can delete only their own tasks"
        )

    return delete_task(
        db,
        task
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

    if current_user.role == "employee" and task.assigned_to != current_user.id:

        raise HTTPException(

            status_code=403,

            detail="Employees can update only assigned tasks"
        )

    if current_user.role == "manager":

        if (

            task.created_by != current_user.id

            and

            task.assigned_to != current_user.id
        ):

            raise HTTPException(

                status_code=403,

                detail="Managers can update only related tasks"
            )

    current_status = (
        task.status
    )

    # EMPLOYEE
    # CANNOT DIRECTLY
    # COMPLETE TASKS

    if (

        current_user.role == "employee"

        and

        status_data.status == "done"
    ):

        raise HTTPException(

            status_code=403,

            detail=
            "Employees cannot move tasks directly to done"
        )

    allowed_statuses = (

        VALID_TRANSITIONS.get(
            current_status,
            []
        )
    )

    if (

        status_data.status
        not in allowed_statuses
    ):

        raise HTTPException(

            status_code=400,

            detail=
            "Invalid workflow transition"
        )

    task.status = (
        status_data.status
    )

    # CREATE APPROVAL
    # WHEN TASK MOVES
    # TO REVIEW

    if status_data.status == "review":

        approval = Approval(

            title=f"Approval request for task #{task.id}",

            description=(
                f"Task '{task.title}' moved to review and requires approval."
            ),

            task_id=task.id,

            requested_by=current_user.id,

            status="pending",

            current_level="manager"
        )

        db.add(approval)

    history = TaskHistory(

        task_id=task.id,

        old_status=
            current_status,

        new_status=
            status_data.status,

        changed_by=
            current_user.id
    )

    db.add(history)

    db.commit()

    db.refresh(task)

    return task


def fetch_task_status_history(db: Session, task_id: int, current_user):

    task = get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role == "employee" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Employees can view only assigned task history")

    if current_user.role == "manager":
        if task.created_by != current_user.id and task.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Managers can view only related task history")

    return db.query(TaskHistory).filter(
        TaskHistory.task_id == task_id
    ).order_by(
        TaskHistory.created_at.desc()
    ).all()
