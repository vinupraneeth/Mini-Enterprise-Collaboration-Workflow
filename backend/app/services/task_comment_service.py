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
