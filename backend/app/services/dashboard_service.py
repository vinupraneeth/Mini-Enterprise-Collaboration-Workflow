from sqlalchemy import func, select

from app.models.task_model import Task

from app.models.approval_model import (
    Approval
)

from app.models.task_comment_model import (
    TaskComment
)


def count_records(
    db,
    model,
    *conditions
):

    statement = select(
        func.count(model.id)
    )

    if conditions:

        statement = statement.where(
            *conditions
        )

    return db.execute(statement).scalar_one()


def get_dashboard_analytics(
    db,
    current_user
):

    role = current_user.role.lower()

    task_conditions = []

    approval_conditions = []

    # ADMIN

    if role == "admin":

        pass

    # MANAGER

    elif role == "manager":

        task_conditions.append(
            Task.created_by ==
            current_user.id
        )

        approval_conditions.append(
            Approval.reviewed_by ==
            current_user.id
        )

    # EMPLOYEE

    elif role == "employee":

        task_conditions.append(
            Task.assigned_to ==
            current_user.id
        )

        approval_conditions.append(
            Approval.requested_by ==
            current_user.id
        )

    total_tasks = count_records(
        db,
        Task,
        *task_conditions
    )

    todo_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "todo"
    )

    in_progress_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "in_progress"
    )

    review_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "review"
    )

    done_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "done"
    )

    pending_approvals = count_records(
        db,
        Approval,
        *approval_conditions,
        Approval.status == "pending"
    )

    approved_approvals = count_records(
        db,
        Approval,
        *approval_conditions,
        Approval.status.in_(
            [
                "approved",
                "manager_approved",
                "admin_approved"
            ]
        )
    )

    rejected_approvals = count_records(
        db,
        Approval,
        *approval_conditions,
        Approval.status == "rejected"
    )

    total_comments = count_records(
        db,
        TaskComment
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


def get_ai_summary(
    db,
    current_user
):

    role = current_user.role.lower()

    task_conditions = []

    if role == "manager":

        task_conditions.append(
            Task.created_by ==
            current_user.id
        )

    elif role == "employee":

        task_conditions.append(
            Task.assigned_to ==
            current_user.id
        )

    pending_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status != "done"
    )

    high_priority_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.priority == "high",
        Task.status != "done"
    )

    delayed_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.due_date < func.now(),
        Task.status != "done"
    )

    insights = [
        f"{pending_tasks} pending tasks need attention.",
        f"{high_priority_tasks} high priority tasks are pending.",
        f"{delayed_tasks} delayed tasks are past their due date."
    ]

    if pending_tasks == 0:

        insights.append(
            "All visible tasks are completed."
        )

    return {

        "pending_tasks": pending_tasks,

        "high_priority_tasks": high_priority_tasks,

        "delayed_tasks": delayed_tasks,

        "insights": insights
    }
