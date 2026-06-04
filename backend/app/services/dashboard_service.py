from sqlalchemy import func, or_, select

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


def get_task_conditions(current_user):

    role = current_user.role.lower()

    if role == "manager":

        return [
            or_(
                Task.created_by == current_user.id,
                Task.assigned_to == current_user.id
            )
        ]

    if role == "employee":

        return [
            Task.assigned_to == current_user.id
        ]

    return []


def get_visible_task_ids(
    db,
    current_user,
    *task_conditions
):

    statement = select(Task.id)

    if task_conditions:

        statement = statement.where(
            *task_conditions
        )

    return db.execute(
        statement
    ).scalars().all()


def count_visible_comments(
    db,
    current_user,
    *task_conditions
):

    if current_user.role.lower() == "admin":

        return count_records(
            db,
            TaskComment
        )

    task_ids = get_visible_task_ids(
        db,
        current_user,
        *task_conditions
    )

    if not task_ids:

        return 0

    comment_conditions = [
        TaskComment.task_id.in_(task_ids)
    ]

    if current_user.role.lower() == "employee":

        comment_conditions.append(
            TaskComment.is_internal.is_(False)
        )

    return count_records(
        db,
        TaskComment,
        *comment_conditions
    )


def count_pending_approvals(
    db,
    current_user
):

    role = current_user.role.lower()

    active_statuses = [
        "pending",
        "manager_approved",
        "hold"
    ]

    statement = select(
        func.count(Approval.id)
    )

    if role == "admin":

        statement = statement.where(
            Approval.current_level == "admin",
            Approval.status.in_(
                active_statuses
            )
        )

    elif role == "manager":

        statement = statement.outerjoin(
            Task,
            Approval.task_id == Task.id
        ).where(
            Approval.current_level == "manager",
            Approval.requested_by != current_user.id,
            Approval.status.in_(
                [
                    "pending",
                    "hold"
                ]
            ),
            or_(
                Task.created_by == current_user.id,
                Task.assigned_to == current_user.id
            )
        )

    elif role == "employee":

        statement = statement.where(
            Approval.requested_by == current_user.id,
            Approval.current_level != "completed",
            Approval.status.in_(
                active_statuses
            )
        )

    else:

        return 0

    return db.execute(
        statement
    ).scalar_one()


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

        task_conditions.extend(
            get_task_conditions(
                current_user
            )
        )

        approval_conditions.append(
            Approval.reviewed_by ==
            current_user.id
        )

    # EMPLOYEE

    elif role == "employee":

        task_conditions.extend(
            get_task_conditions(
                current_user
            )
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

    pending_approvals = count_pending_approvals(
        db,
        current_user
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

    total_comments = count_visible_comments(
        db,
        current_user,
        *task_conditions
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

    task_conditions = get_task_conditions(
        current_user
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
