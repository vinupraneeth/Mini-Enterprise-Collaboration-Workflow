from datetime import datetime

from sqlalchemy import or_, select

from app.models.task_history_model import (
    TaskHistory
)

from app.models.task_model import (
    Task
)

from app.models.task_comment_model import (
    TaskComment
)

from app.models.approval_model import (
    Approval
)

from app.models.approval_history_model import (
    ApprovalHistory
)

from app.models.audit_log_model import (
    AuditLog
)


def get_visible_task_ids(
    db,
    current_user
):

    if current_user.role == "admin":

        return None

    statement = select(Task.id)

    if current_user.role == "manager":

        statement = statement.where(
            or_(
                Task.created_by == current_user.id,
                Task.assigned_to == current_user.id
            )
        )

    elif current_user.role == "employee":

        statement = statement.where(
            Task.assigned_to == current_user.id
        )

    else:

        return []

    return db.execute(
        statement
    ).scalars().all()


def fetch_activity_feed(
    db,
    current_user
):

    activities = []

    visible_task_ids = get_visible_task_ids(
        db,
        current_user
    )

    task_history_statement = (
        select(TaskHistory)
    )

    if visible_task_ids is not None:

        if not visible_task_ids:

            task_history = []

        else:

            task_history_statement = task_history_statement.where(
                TaskHistory.task_id.in_(
                    visible_task_ids
                )
            )

    if visible_task_ids is None or visible_task_ids:

        task_history = db.execute(
            task_history_statement
        ).scalars().all()

    for item in task_history:

        activities.append({

            "type": "task_status",

            "message":
            f"Task #{item.task_id} moved from {item.old_status} to {item.new_status}",

            "created_at":
            item.created_at
        })

    comment_statement = (
        select(TaskComment)
    )

    if visible_task_ids == []:

        comments = []

    else:

        if visible_task_ids is not None:

            comment_statement = comment_statement.where(
                TaskComment.task_id.in_(
                    visible_task_ids
                )
            )

        if current_user.role == "employee":

            comment_statement = comment_statement.where(
                TaskComment.is_internal.is_(False)
            )

        comments = db.execute(
            comment_statement
        ).scalars().all()

    for item in comments:

        message = (
            f"Internal note added on Task #{item.task_id}"
            if item.is_internal
            else
            f"Comment added on Task #{item.task_id}"
        )

        activities.append({

            "type": "comment",

            "message":
            message,

            "created_at":
            item.created_at
        })

    approval_history_statement = (
        select(ApprovalHistory)
    )

    if current_user.role != "admin":

        approval_history_statement = approval_history_statement.join(
            Approval,
            ApprovalHistory.approval_id == Approval.id
        )

        visibility_conditions = [
            Approval.requested_by == current_user.id,
            Approval.reviewed_by == current_user.id,
            ApprovalHistory.action_by == current_user.id
        ]

        if visible_task_ids:

            visibility_conditions.append(
                Approval.task_id.in_(
                    visible_task_ids
                )
            )

        approval_history_statement = approval_history_statement.where(
            or_(
                *visibility_conditions
            )
        )

    approval_history = db.execute(
        approval_history_statement
    ).scalars().all()

    for item in approval_history:

        activities.append({

            "type": "approval",

            "message":
            f"Approval #{item.approval_id} changed from {item.old_status} to {item.new_status}",

            "created_at":
            item.created_at
        })

    audit_statement = (
        select(AuditLog)
    )

    audit_actions = [
        "created task",
        "updated task",
        "assigned task",
        "deleted task",
        "uploaded document",
        "downloaded document"
    ]

    audit_statement = audit_statement.where(
        AuditLog.action.in_(
            audit_actions
        )
    )

    if current_user.role != "admin":

        audit_statement = audit_statement.where(
            AuditLog.user_id == current_user.id
        )

    audit_logs = db.execute(
        audit_statement
    ).scalars().all()

    for item in audit_logs:

        activities.append({

            "type": "audit",

            "message":
            f"{item.action.title()} on {item.entity} #{item.entity_id}",

            "created_at":
            item.timestamp
        })

    activities.sort(

        key=lambda x: x["created_at"] or datetime.min,

        reverse=True
    )

    return activities
