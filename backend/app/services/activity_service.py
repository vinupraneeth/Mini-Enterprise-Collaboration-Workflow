from app.models.task_history_model import (
    TaskHistory
)

from app.models.task_comment_model import (
    TaskComment
)

from app.models.approval_history_model import (
    ApprovalHistory
)


def fetch_activity_feed(
    db
):

    activities = []

    task_history = db.query(
        TaskHistory
    ).all()

    for item in task_history:

        activities.append({

            "type": "task_status",

            "message":
            f"Task {item.task_id} moved from {item.old_status} to {item.new_status}",

            "created_at":
            item.created_at
        })

    comments = db.query(
        TaskComment
    ).all()

    for item in comments:

        activities.append({

            "type": "comment",

            "message":
            f"Comment added on Task {item.task_id}",

            "created_at":
            item.created_at
        })

    approval_history = db.query(
        ApprovalHistory
    ).all()

    for item in approval_history:

        activities.append({

            "type": "approval",

            "message":
            f"Approval {item.approval_id} changed from {item.old_status} to {item.new_status}",

            "created_at":
            item.created_at
        })

    activities.sort(

        key=lambda x: x["created_at"],

        reverse=True
    )

    return activities