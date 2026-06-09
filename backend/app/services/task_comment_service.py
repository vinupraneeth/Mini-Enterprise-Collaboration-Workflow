from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.task_comment_model import (
    TaskComment
)

from app.repositories.task_repository import (
    get_task_by_id
)

from app.repositories.task_comment_repository import (
    create_comment,
    get_comments_by_task
)

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.notification_service import (
    create_notification
)

from app.core.cache import (
    invalidate_dashboard_cache
)


def check_task_access(
    task,
    current_user
):

    if current_user.role == "admin":

        return

    if current_user.role == "manager":

        if (
            task.created_by == current_user.id
            or
            task.assigned_to == current_user.id
        ):

            return

    if current_user.role == "employee" and task.assigned_to == current_user.id:

        return

    raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )


def add_comment_to_task(
    db: Session,
    task_id: int,
    comment_data,
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

    check_task_access(
        task,
        current_user
    )

    if current_user.role == "employee" and comment_data.is_internal:
        raise HTTPException(
            status_code=403,
            detail="Employees cannot create internal comments"
        )

    comment = TaskComment(

        task_id=task_id,

        user_id=current_user.id,

        comment=comment_data.comment,

        is_internal=
            comment_data.is_internal
    )

    create_comment(
        db,
        comment
    )

    action_text = (
        "added internal note"
        if comment_data.is_internal
        else
        "added comment"
    )

    create_audit_log(
        db,
        current_user.id,
        action_text,
        "task",
        task_id
    )

    message = (
        f"Internal note added on task #{task_id}."
        if comment_data.is_internal
        else
        f"Comment added on task #{task_id}."
    )

    notified_users = set()

    if comment_data.is_internal:

        if task.created_by and task.created_by != current_user.id:

            create_notification(
                db,
                task.created_by,
                message
            )

    else:

        if task.created_by and task.created_by != current_user.id:

            create_notification(
                db,
                task.created_by,
                message
            )

            notified_users.add(task.created_by)

        if (
            task.assigned_to
            and
            task.assigned_to != current_user.id
            and
            task.assigned_to not in notified_users
        ):

            create_notification(
                db,
                task.assigned_to,
                message
            )

    db.commit()

    invalidate_dashboard_cache()

    comments = get_comments_by_task(
        db,
        task_id
    )

    return comments[0]


def fetch_task_comments(
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

    check_task_access(
        task,
        current_user
    )

    comments = get_comments_by_task(
        db,
        task_id
    )

    # EMPLOYEE
    # CANNOT SEE INTERNAL NOTES

    if current_user.role == "employee":

        comments = [

            comment

            for comment in comments

            if not comment[
                "is_internal"
            ]
        ]

    return comments
