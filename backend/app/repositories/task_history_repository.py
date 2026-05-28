from app.models.task_history_model import (
    TaskHistory
)


def create_task_history(
    db,
    task_id,
    old_status,
    new_status,
    changed_by
):

    history = TaskHistory(

        task_id=task_id,

        old_status=old_status,

        new_status=new_status,

        changed_by=changed_by
    )

    db.add(history)

    db.commit()

    db.refresh(history)

    return history