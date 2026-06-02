from fastapi import HTTPException

from sqlalchemy import select

from app.models.notification_model import Notification


def create_notification(
    db,
    user_id,
    message
):

    notification = Notification(

        user_id=user_id,

        message=message,

        is_read=False
    )

    db.add(notification)

    return notification


def fetch_notifications(
    db,
    current_user
):

    return db.execute(
        get_notifications_statement(current_user)
    ).scalars().all()


def get_notifications_statement(
    current_user
):

    statement = select(Notification).where(
        Notification.user_id == current_user.id
    )

    if current_user.role == "employee":

        statement = statement.where(
            ~Notification.message.ilike(
                "Internal note%"
            )
        )

    return statement.order_by(
        Notification.created_at.desc()
    )


def mark_notification_read(
    db,
    notification_id,
    current_user
):

    notification = db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).scalar_one_or_none()

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()

    db.refresh(notification)

    return notification
