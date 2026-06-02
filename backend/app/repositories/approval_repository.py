from sqlalchemy import select

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

    result = db.execute(
        select(Approval).where(
            Approval.id == approval_id
        )
    )

    return result.scalar_one_or_none()


def get_all_approvals(
    db: Session
):

    result = db.execute(
        select(Approval)
    )

    return result.scalars().all()


def update_approval(
    db: Session,
    approval: Approval
):

    db.commit()

    db.refresh(approval)

    return approval
