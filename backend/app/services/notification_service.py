from app.utils.db_exceptions import (
    handle_db_commit
)

from fastapi import HTTPException

from sqlalchemy import select

from app.models.notification_model import Notification

from app.models.workflow_governance_model import (
    NotificationPreference
)

from app.services.websocket_manager import (
    manager
)

from app.services.audit_log_service import (
    create_audit_log
)

import asyncio


def notification_allowed_for_user(
    db,
    user_id,
    notification_type
):

    preference = db.execute(
        select(NotificationPreference).where(
            NotificationPreference.user_id == user_id
        )
    ).scalar_one_or_none()

    if not preference:

        return True

    if not preference.in_app_enabled:

        return False

    if notification_type == "task":

        return preference.task_notifications

    if notification_type == "approval":

        return preference.approval_notifications

    if notification_type == "escalation":

        return preference.escalation_notifications

    if notification_type == "document":

        return preference.document_notifications

    return True


def dispatch_websocket_message(
    user_id,
    payload
):

    if not manager.loop:

        return

    asyncio.run_coroutine_threadsafe(
        manager.send_message(
            user_id,
            payload
        ),
        manager.loop
    )


def dispatch_kanban_update(
    user_ids
):

    if not manager.loop:

        return

    asyncio.run_coroutine_threadsafe(
        manager.broadcast_to_users(
            user_ids,
            {
                "type": "kanban_updated",
                "message": "Kanban board updated"
            }
        ),
        manager.loop
    )


def create_notification(
    db,
    user_id,
    message,
    notification_type=None,
    priority="medium"
):

    if not notification_allowed_for_user(
        db,
        user_id,
        notification_type
    ):

        return None

    notification = Notification(

        user_id=user_id,

        message=message,

        notification_type=notification_type,

        priority=priority,

        is_read=False
    )

    db.add(notification)

    dispatch_websocket_message(
        user_id,
        {
            "type": "notification",
            "message": message,
            "notification": {
                "user_id": user_id,
                "message": message,
                "notification_type": notification_type,
                "priority": priority,
                "is_read": False
            }
        }
    )

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

    create_audit_log(
        db,
        current_user.id,
        "read notification",
        "notification",
        notification.id
    )

    handle_db_commit(db)

    db.refresh(notification)

    return notification
