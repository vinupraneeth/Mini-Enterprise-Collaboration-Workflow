from sqlalchemy import select

from sqlalchemy.orm import Session

from app.models.task_comment_model import (
    TaskComment
)

from app.models.user_model import (
    User
)


def create_comment(
    db: Session,
    comment: TaskComment
):

    db.add(comment)

    db.commit()

    db.refresh(comment)

    return comment


def get_comments_by_task(
    db: Session,
    task_id: int
):

    comments = db.execute(

        select(

            TaskComment,

            User.name

        ).join(

            User,

            TaskComment.user_id
            == User.id

        ).where(

            TaskComment.task_id
            == task_id

        ).order_by(

            TaskComment.created_at
            .desc()
        )
    ).all()

    return [

        {

            "id":
                comment.id,

            "task_id":
                comment.task_id,

            "user_id":
                comment.user_id,

            "user_name":
                user_name,

            "comment":
                comment.comment,

            "is_internal":
                comment.is_internal,

            "created_at":
                comment.created_at
        }

        for comment,
        user_name

        in comments
    ]
