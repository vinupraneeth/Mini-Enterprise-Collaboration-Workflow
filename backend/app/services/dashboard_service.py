from app.models.task_model import Task

from app.models.approval_model import (
    Approval
)

from app.models.task_comment_model import (
    TaskComment
)


def get_dashboard_analytics(
    db,
    current_user
):

    role = current_user.role.lower()

    task_query = db.query(Task)

    approval_query = db.query(
        Approval
    )

    comment_query = db.query(
        TaskComment
    )

    # ADMIN

    if role == "admin":

        pass

    # MANAGER

    elif role == "manager":

        task_query = task_query.filter(
            Task.created_by ==
            current_user.id
        )

        approval_query = (
            approval_query.filter(
                Approval.reviewed_by ==
                current_user.id
            )
        )

    # EMPLOYEE

    elif role == "employee":

        task_query = task_query.filter(
            Task.assigned_to ==
            current_user.id
        )

        approval_query = (
            approval_query.filter(
                Approval.requested_by ==
                current_user.id
            )
        )

    total_tasks = task_query.count()

    todo_tasks = task_query.filter(
        Task.status == "todo"
    ).count()

    in_progress_tasks = (
        task_query.filter(
            Task.status ==
            "in_progress"
        ).count()
    )

    review_tasks = (
        task_query.filter(
            Task.status ==
            "review"
        ).count()
    )

    done_tasks = (
        task_query.filter(
            Task.status == "done"
        ).count()
    )

    pending_approvals = (
        approval_query.filter(
            Approval.status ==
            "pending"
        ).count()
    )

    approved_approvals = (
        approval_query.filter(
            Approval.status ==
            "approved"
        ).count()
    )

    rejected_approvals = (
        approval_query.filter(
            Approval.status ==
            "rejected"
        ).count()
    )

    total_comments = (
        comment_query.count()
    )

    return {

        "role": role,

        "tasks": {

            "total": total_tasks,

            "todo": todo_tasks,

            "in_progress":
            in_progress_tasks,

            "review":
            review_tasks,

            "done": done_tasks
        },

        "approvals": {

            "pending":
            pending_approvals,

            "approved":
            approved_approvals,

            "rejected":
            rejected_approvals
        },

        "comments": {

            "total": total_comments
        }
    }