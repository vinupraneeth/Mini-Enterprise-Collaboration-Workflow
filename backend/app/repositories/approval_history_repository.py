from app.models.approval_history_model import (
    ApprovalHistory
)


def create_approval_history(

    db,

    approval_id,

    old_status,

    new_status,

    changed_by
):

    history = ApprovalHistory(

        approval_id=approval_id,

        old_status=old_status,

        new_status=new_status,

        changed_by=changed_by
    )

    db.add(history)

    db.commit()

    db.refresh(history)

    return history