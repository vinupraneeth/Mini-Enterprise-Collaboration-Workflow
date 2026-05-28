from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.approval_model import Approval

from app.models.approval_history_model import ApprovalHistory

from app.models.task_model import Task

from app.schemas.approval_schema import ApprovalCreate, ApprovalReview


def manager_can_access_approval(
    db: Session,
    approval: Approval,
    current_user
):

    if approval.task_id is None:

        return approval.current_level == "manager"

    task = db.query(Task).filter(
        Task.id == approval.task_id
    ).first()

    if not task:

        return False

    return (
        task.created_by == current_user.id
        or
        task.assigned_to == current_user.id
    )


def create_approval_history(
        
    db: Session,

    approval_id: int,

    action_by: int,

    action: str,

    comment: str | None = None
):
    history = ApprovalHistory(

        approval_id=approval_id,

        action_by=action_by,

        action=action,

        old_status=action,

        new_status=action,

        changed_by=action_by,
        
        comment=comment
    )

    db.add(history)

    return history


def create_approval_request(
    db: Session,
    approval_data: ApprovalCreate,
    current_user
):
    if approval_data.task_id is not None:
        task = db.query(Task).filter(
            Task.id == approval_data.task_id
        ).first()

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

    approval = Approval(

        title=approval_data.title,

        description=approval_data.description,

        task_id=approval_data.task_id,

        requested_by=current_user.id,

        status="pending",

        current_level="manager",

        remarks=None
    )

    db.add(approval)
    db.flush()

    create_approval_history(

        db=db,

        approval_id=approval.id,

        action_by=current_user.id,

        action="submitted",

        comment="Approval request submitted"
    )

    db.commit()
    db.refresh(approval)

    return approval


def fetch_approvals(
        
    db: Session,
    current_user
):
    query = db.query(Approval)

    if current_user.role == "admin":
        return query.order_by(
            Approval.created_at.desc()
        ).all()

    if current_user.role == "manager":

        approvals = query.filter(
            Approval.current_level == "manager"
        ).order_by(
            Approval.created_at.desc()
        ).all()

        return [

            approval

            for approval in approvals

            if manager_can_access_approval(
                db,
                approval,
                current_user
            )
        ]

    if current_user.role == "employee":
        return query.filter(
            Approval.requested_by == current_user.id
        ).order_by(
            Approval.created_at.desc()
        ).all()

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
    approval = db.query(Approval).filter(
        Approval.id == approval_id
    ).first()

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

    if approval.current_level == "manager":
        if action == "approve":
            approval.status = "manager_approved"
            approval.current_level = "admin"

        elif action == "reject":
            approval.status = "rejected"
            approval.current_level = "completed"

        elif action == "hold":
            approval.status = "hold"
            approval.current_level = "manager"

    elif approval.current_level == "admin":
        if action == "approve":
            approval.status = "admin_approved"
            approval.current_level = "completed"

            if approval.task_id is not None:
                task = db.query(Task).filter(
                    Task.id == approval.task_id
                ).first()

                if task:
                    task.status = "done"

        elif action == "reject":
            approval.status = "rejected"
            approval.current_level = "completed"

        elif action == "hold":
            approval.status = "hold"
            approval.current_level = "admin"

    create_approval_history(

        db=db,
        approval_id=approval.id,
        action_by=current_user.id,
        action=action,
        comment=comment
    )

    db.commit()
    db.refresh(approval)

    return approval


def fetch_approval_history(
    db: Session,
    approval_id: int,
    current_user
):
    approval = db.query(Approval).filter(
        Approval.id == approval_id
    ).first()

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

        if not manager_can_access_approval(
            db,
            approval,
            current_user
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

    return db.query(ApprovalHistory).filter(
        ApprovalHistory.approval_id == approval_id
    ).order_by(
        ApprovalHistory.created_at.desc()
    ).all()
