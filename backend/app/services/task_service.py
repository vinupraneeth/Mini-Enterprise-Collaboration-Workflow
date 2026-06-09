from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.task_model import Task

from app.models.task_history_model import (
    TaskHistory
)

from app.models.approval_model import (
    Approval
)

from app.models.approval_history_model import (
    ApprovalHistory
)

from app.models.user_model import (
    User
)

from sqlalchemy import desc, select

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

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.notification_service import (
    create_notification,
    dispatch_kanban_update
)

from app.core.cache import (
    invalidate_dashboard_cache
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


def get_task_related_user_ids(
    task,
    *extra_user_ids
):

    user_ids = set()

    if task.created_by:

        user_ids.add(
            task.created_by
        )

    if task.assigned_to:

        user_ids.add(
            task.assigned_to
        )

    for user_id in extra_user_ids:

        if user_id:

            user_ids.add(
                user_id
            )

    return list(user_ids)


def attach_task_user_names(
    db: Session,
    tasks
):

    user_ids = set()

    for task in tasks:

        if task.assigned_to:

            user_ids.add(task.assigned_to)

        if task.created_by:

            user_ids.add(task.created_by)

    if not user_ids:

        return tasks

    users = db.execute(
        select(User).where(
            User.id.in_(user_ids)
        )
    ).scalars().all()

    user_map = {

        user.id: user.name

        for user in users
    }

    for task in tasks:

        task.assigned_to_name = user_map.get(
            task.assigned_to
        )

        task.created_by_name = user_map.get(
            task.created_by
        )

    return tasks


def validate_assignment(

    db: Session,

    assigned_to: int,

    current_user
):

    assigned_user = db.execute(
        select(User).where(
            User.id == assigned_to
        )
    ).scalar_one_or_none()

    if not assigned_user:

        raise HTTPException(

            status_code=404,

            detail="Assigned user not found"
        )

    if assigned_user.role != "employee":

        raise HTTPException(

            status_code=403,

            detail="Tasks can be assigned only to employees"
        )

    if (
        current_user.organization_id
        and
        assigned_user.organization_id != current_user.organization_id
    ):

        raise HTTPException(

            status_code=403,

            detail="Tasks can be assigned only within your organization"
        )

    return assigned_user


def get_organization_user_ids(
    db: Session,
    current_user
):

    if not current_user.organization_id:

        return []

    return db.execute(
        select(User.id).where(
            User.organization_id ==
            current_user.organization_id
        )
    ).scalars().all()


def task_in_current_organization(
    db: Session,
    task,
    current_user
):

    if not current_user.organization_id:

        return True

    organization_user_ids = get_organization_user_ids(
        db,
        current_user
    )

    return (
        task.created_by in organization_user_ids
        or
        task.assigned_to in organization_user_ids
    )


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

    task = create_task(

        db,

        task,

        current_user.id
    )

    create_audit_log(
        db,
        current_user.id,
        "created task",
        "task",
        task.id
    )

    create_notification(
        db,
        task.assigned_to,
        f"You have been assigned task #{task.id}: {task.title}"
    )

    db.commit()

    invalidate_dashboard_cache()

    dispatch_kanban_update(
        get_task_related_user_ids(
            task,
            current_user.id
        )
    )

    return task


def fetch_tasks(

    db: Session,

    current_user
):

    tasks = get_all_tasks(db)

    if current_user.role == "admin":

        filtered_tasks = [

            task

            for task in tasks

            if task_in_current_organization(
                db,
                task,
                current_user
            )
        ]

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

        latest_approval = db.execute(
            select(Approval).where(

                Approval.task_id == task.id

            ).order_by(

                desc(Approval.id)
            ).limit(1)
        ).scalar_one_or_none()

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

    return attach_task_user_names(
        db,
        filtered_tasks
    )


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

    if not task_in_current_organization(
        db,
        task,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
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

    attach_task_user_names(
        db,
        [task]
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

    old_assigned_to = (
        task.assigned_to
        if task
        else None
    )

    if not task:

        raise HTTPException(

            status_code=404,

            detail="Task not found"
        )

    if not task_in_current_organization(
        db,
        task,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
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

    create_audit_log(
        db,
        current_user.id,
        "assigned task",
        "task",
        task.id
    )

    create_notification(
        db,
        task.assigned_to,
        f"You have been assigned task #{task.id}: {task.title}"
    )

    db.commit()

    invalidate_dashboard_cache()

    dispatch_kanban_update(
        get_task_related_user_ids(
            task,
            current_user.id,
            old_assigned_to
        )
    )

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

    old_assigned_to = (
        task.assigned_to
        if task
        else None
    )

    if not task:

        raise HTTPException(

            status_code=404,

            detail="Task not found"
        )

    if not task_in_current_organization(
        db,
        task,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
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

    task = update_task(
        db,
        task,
        task_data,
        current_user.id
    )

    create_audit_log(
        db,
        current_user.id,
        "updated task",
        "task",
        task.id
    )

    create_notification(
        db,
        task.assigned_to,
        f"Task #{task.id} was updated: {task.title}"
    )

    db.commit()

    invalidate_dashboard_cache()

    dispatch_kanban_update(
        get_task_related_user_ids(
            task,
            current_user.id,
            old_assigned_to
        )
    )

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

    if not task_in_current_organization(
        db,
        task,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
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

    create_audit_log(
        db,
        current_user.id,
        "deleted task",
        "task",
        task.id
    )

    related_user_ids = get_task_related_user_ids(
        task,
        current_user.id
    )

    deleted_task = delete_task(
        db,
        task
    )

    invalidate_dashboard_cache()

    dispatch_kanban_update(
        related_user_ids
    )

    return deleted_task


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

    if not task_in_current_organization(
        db,
        task,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
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

    if (

        status_data.status == "review"

        and

        (
            current_user.role != "employee"
            or
            task.assigned_to != current_user.id
        )
    ):

        raise HTTPException(

            status_code=403,

            detail="Only the assigned employee can submit a task for review"
        )

    if (

        current_status == "review"

        and

        status_data.status == "done"
    ):

        latest_approval = db.execute(
            select(Approval).where(

                Approval.task_id == task.id

            ).order_by(

                desc(Approval.id)
            ).limit(1)
        ).scalar_one_or_none()

        if (
            not latest_approval
            or
            latest_approval.current_level != "completed"
            or
            latest_approval.status not in [
                "manager_approved",
                "admin_approved"
            ]
        ):

            raise HTTPException(

                status_code=403,

                detail="Task can move to done only after approval is completed"
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

        creator = db.execute(
            select(User).where(
                User.id == task.created_by
            )
        ).scalar_one_or_none()

        approval_level = (
            "admin"
            if creator and creator.role == "admin"
            else "manager"
        )

        approval = Approval(

            title=f"Approval request for task #{task.id}",

            description=(
                f"Task '{task.title}' moved to review and requires approval."
            ),

            task_id=task.id,

            requested_by=current_user.id,

            status="pending",

            current_level=approval_level
        )

        db.add(approval)

        db.flush()

        approval_history = ApprovalHistory(

            approval_id=approval.id,

            action_by=current_user.id,

            action="submitted",

            old_status="submitted",

            new_status="submitted",

            changed_by=current_user.id,

            comment="Task moved to review"
        )

        db.add(approval_history)

        if task.created_by:

            create_notification(
                db,
                task.created_by,
                f"Task #{task.id} is ready for review."
            )

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

    create_audit_log(
        db,
        current_user.id,
        f"changed task status from {current_status} to {status_data.status}",
        "task",
        task.id
    )

    if task.created_by and task.created_by != current_user.id:

        create_notification(
            db,
            task.created_by,
            f"Task #{task.id} status changed to {status_data.status}."
        )

    if task.assigned_to and task.assigned_to != current_user.id:

        create_notification(
            db,
            task.assigned_to,
            f"Task #{task.id} status changed to {status_data.status}."
        )

    db.commit()

    invalidate_dashboard_cache()

    dispatch_kanban_update(
        get_task_related_user_ids(
            task,
            current_user.id
        )
    )

    db.refresh(task)

    return task


def fetch_task_status_history(db: Session, task_id: int, current_user):

    return db.execute(
        get_task_status_history_statement(
            db,
            task_id,
            current_user
        )
    ).scalars().all()


def get_task_status_history_statement(db: Session, task_id: int, current_user):

    task = get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if not task_in_current_organization(
        db,
        task,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if current_user.role == "employee" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Employees can view only assigned task history")

    if current_user.role == "manager":
        if task.created_by != current_user.id and task.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Managers can view only related task history")

    return select(TaskHistory).where(
        TaskHistory.task_id == task_id
    ).order_by(
        TaskHistory.created_at.desc()
    )
