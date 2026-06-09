from fastapi import HTTPException

from sqlalchemy import and_, or_, select

from sqlalchemy.orm import Session

from app.models.approval_model import Approval

from app.models.approval_history_model import ApprovalHistory

from app.models.task_model import Task

from app.models.task_history_model import TaskHistory

from app.models.user_model import User

from app.schemas.approval_schema import ApprovalCreate, ApprovalReview

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.notification_service import (
    create_notification
)

from app.core.cache import (
    invalidate_dashboard_cache
)


def manager_can_access_approval(
    db: Session,
    approval: Approval,
    current_user
):

    if approval.task_id is None:

        return (
            approval.current_level == "manager"
            and
            approval.requested_by != current_user.id
        )

    task = db.execute(
        select(Task).where(
            Task.id == approval.task_id
        )
    ).scalar_one_or_none()

    if not task:

        return False

    return (
        approval.requested_by != current_user.id
        and
        (
            task.created_by == current_user.id
            or
            task.assigned_to == current_user.id
        )
    )


def create_approval_history(
        
    db: Session,

    approval_id: int,

    action_by: int,

    action: str,

    comment: str | None = None,

    old_status: str | None = None,

    new_status: str | None = None
):
    history = ApprovalHistory(

        approval_id=approval_id,

        action_by=action_by,

        action=action,

        old_status=old_status or action,

        new_status=new_status or action,

        changed_by=action_by,
        
        comment=comment
    )

    db.add(history)

    return history


def update_task_status_after_approval(
    db: Session,
    task: Task,
    new_status: str,
    current_user
):

    if task.status == new_status:

        return

    old_status = task.status

    task.status = new_status

    history = TaskHistory(

        task_id=task.id,

        old_status=old_status,

        new_status=new_status,

        changed_by=current_user.id
    )

    db.add(history)

    create_audit_log(
        db,
        current_user.id,
        f"changed task status from {old_status} to {new_status}",
        "task",
        task.id
    )

    notified_users = set()

    if task.assigned_to and task.assigned_to != current_user.id:

        create_notification(
            db,
            task.assigned_to,
            f"Task #{task.id} status changed to {new_status}."
        )

        notified_users.add(task.assigned_to)

    if (
        task.created_by
        and
        task.created_by != current_user.id
        and
        task.created_by not in notified_users
    ):

        create_notification(
            db,
            task.created_by,
            f"Task #{task.id} status changed to {new_status}."
        )


def create_approval_request(
    db: Session,
    approval_data: ApprovalCreate,
    current_user
):
    task = None

    if current_user.role == "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin users review approvals and cannot raise approval requests"
        )

    if approval_data.task_id is not None:
        task = db.execute(
            select(Task).where(
                Task.id == approval_data.task_id
            )
        ).scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        if current_user.role == "employee" and task.assigned_to != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Employees can request approval only for assigned tasks"
            )

        if current_user.role == "manager":
            if task.created_by != current_user.id and task.assigned_to != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Managers can request approval only for related tasks"
                )

    current_level = "manager"

    if task is None:

        current_level = "admin"

    approval = Approval(

        title=approval_data.title,

        description=approval_data.description,

        task_id=approval_data.task_id,

        requested_by=current_user.id,

        status="pending",

        current_level=current_level,

        remarks=None
    )

    db.add(approval)
    db.flush()

    create_approval_history(

        db=db,

        approval_id=approval.id,

        action_by=current_user.id,

        action="submitted",

        comment="Approval request submitted",

        old_status="new",

        new_status=approval.status
    )

    create_audit_log(
        db,
        current_user.id,
        "submitted approval",
        "approval",
        approval.id
    )

    if task and task.created_by and task.created_by != current_user.id:

        create_notification(
            db,
            task.created_by,
            f"Approval request submitted for task #{task.id}."
        )

    if task is None and approval.current_level == "admin":

        admins = db.execute(
            select(User).where(
                User.role == "admin"
            )
        ).scalars().all()

        for admin in admins:

            if admin.id != current_user.id:

                create_notification(
                    db,
                    admin.id,
                    f"New approval request #{approval.id} is waiting for admin review."
                )

    db.commit()

    invalidate_dashboard_cache()

    db.refresh(approval)

    return approval


def fetch_approvals(
        
    db: Session,
    current_user
):
    return db.execute(
        get_approvals_statement(
            current_user
        )
    ).scalars().all()


def get_approvals_statement(
    current_user
):

    if current_user.role == "admin":

        return select(Approval).order_by(
            Approval.created_at.desc()
        )

    if current_user.role == "manager":

        return select(Approval).outerjoin(
            Task,
            Approval.task_id == Task.id
        ).where(
            or_(
                Approval.requested_by == current_user.id,
                Task.created_by == current_user.id,
                Task.assigned_to == current_user.id,
                and_(
                    Approval.task_id.is_(None),
                    Approval.reviewed_by == current_user.id
                ),
                Approval.id.in_(
                    select(ApprovalHistory.approval_id).where(
                        ApprovalHistory.action_by == current_user.id
                    )
                )
            )
        ).order_by(
            Approval.created_at.desc()
        )

    if current_user.role == "employee":

        return select(Approval).where(
            Approval.requested_by == current_user.id
        ).order_by(
            Approval.created_at.desc()
        )

    raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )


def review_approval_request(
        
    db: Session,
    approval_id: int,
    review_data: ApprovalReview,
    current_user
):
    approval = db.execute(
        select(Approval).where(
            Approval.id == approval_id
        )
    ).scalar_one_or_none()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only Manager or Admin can approve requests"
        )

    if approval.current_level == "completed":
        raise HTTPException(
            status_code=400,
            detail="Approval request is already completed"
        )

    action = review_data.action
    comment = review_data.comment

    if action == "reject" and (not comment or not comment.strip()):
        raise HTTPException(
            status_code=400,
            detail="Rejection requires a comment"
        )

    if approval.current_level == "manager" and current_user.role != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only Manager can act at manager approval level"
        )

    if current_user.role == "manager":

        if not manager_can_access_approval(
            db,
            approval,
            current_user
        ):

            raise HTTPException(
                status_code=403,
                detail="Managers can review only related task approvals"
            )

    if approval.current_level == "admin" and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can act at admin approval level"
        )

    approval.reviewed_by = current_user.id
    approval.remarks = comment

    previous_status = approval.status

    task = None

    if approval.task_id is not None:

        task = db.execute(
            select(Task).where(
                Task.id == approval.task_id
            )
        ).scalar_one_or_none()

    if approval.current_level == "manager":
        if action == "approve":
            approval.status = "manager_approved"

            if (
                task is None
                or
                task.priority == "high"
            ):

                approval.current_level = "admin"

            else:

                approval.current_level = "completed"

                if task:

                    update_task_status_after_approval(
                        db,
                        task,
                        "done",
                        current_user
                    )

        elif action == "reject":
            approval.status = "rejected"
            approval.current_level = "completed"

            if task:

                update_task_status_after_approval(
                    db,
                    task,
                    "in_progress",
                    current_user
                )

        elif action == "hold":
            approval.status = "hold"
            approval.current_level = "manager"

    elif approval.current_level == "admin":
        if action == "approve":
            approval.status = "admin_approved"
            approval.current_level = "completed"

            if task:

                update_task_status_after_approval(
                    db,
                    task,
                    "done",
                    current_user
                )

        elif action == "reject":
            approval.status = "rejected"
            approval.current_level = "completed"

            if task:

                update_task_status_after_approval(
                    db,
                    task,
                    "in_progress",
                    current_user
                )

        elif action == "hold":
            approval.status = "hold"
            approval.current_level = "admin"

    create_approval_history(

        db=db,
        approval_id=approval.id,
        action_by=current_user.id,
        action=action,
        comment=comment,
        old_status=previous_status,
        new_status=approval.status
    )

    action_labels = {

        "approve": "approved",

        "reject": "rejected",

        "hold": "placed on hold"
    }

    audit_labels = {

        "approve": "approved approval",

        "reject": "rejected approval",

        "hold": "held approval"
    }

    create_audit_log(
        db,
        current_user.id,
        audit_labels[action],
        "approval",
        approval.id
    )

    if approval.requested_by != current_user.id:

        create_notification(
            db,
            approval.requested_by,
            f"Your approval request #{approval.id} was {action_labels[action]}."
        )

    if (
        action == "approve"
        and
        approval.current_level == "admin"
    ):

        admins = db.execute(
            select(User).where(
                User.role == "admin"
            )
        ).scalars().all()

        for admin in admins:

            if admin.id != current_user.id:

                create_notification(
                    db,
                    admin.id,
                    f"Approval request #{approval.id} is waiting for final admin review."
                )

    db.commit()

    invalidate_dashboard_cache()

    db.refresh(approval)

    return approval


def fetch_approval_history(
    db: Session,
    approval_id: int,
    current_user
):

    return db.execute(
        get_approval_history_statement(
            db,
            approval_id,
            current_user
        )
    ).scalars().all()


def get_approval_history_statement(
    db: Session,
    approval_id: int,
    current_user
):

    approval = db.execute(
        select(Approval).where(
            Approval.id == approval_id
        )
    ).scalar_one_or_none()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    if current_user.role == "employee" and approval.requested_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Employees can view only their own approval history"
        )

    if current_user.role == "manager":

        if (
            approval.requested_by != current_user.id
            and
            not manager_can_access_approval(
                db,
                approval,
                current_user
            )
        ):

            raise HTTPException(
                status_code=403,
                detail="Managers can view only related approval history"
            )

    if current_user.role not in ["admin", "manager", "employee"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return select(ApprovalHistory).where(
        ApprovalHistory.approval_id == approval_id
    ).order_by(
        ApprovalHistory.created_at.desc()
    )
