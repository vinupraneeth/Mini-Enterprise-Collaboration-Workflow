from sqlalchemy.orm import Session

from app.models.approval_model import (
    Approval
)


def create_approval(
    db: Session,
    approval: Approval
):

    db.add(approval)

    db.commit()

    db.refresh(approval)

    return approval


def get_approval_by_id(
    db: Session,
    approval_id: int
):

    return db.query(Approval).filter(
        Approval.id == approval_id
    ).first()


def get_all_approvals(
    db: Session
):

    return db.query(Approval).all()


def update_approval(
    db: Session,
    approval: Approval
):

    db.commit()

    db.refresh(approval)

    return approval