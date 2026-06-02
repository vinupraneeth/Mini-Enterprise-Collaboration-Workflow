from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user
)

from app.db.deps import get_db

from app.schemas.notification_schema import (
    NotificationResponse
)

from app.services.notification_service import (
    get_notifications_statement,
    mark_notification_read
)


router = APIRouter(

    prefix="/notifications",

    tags=["Notifications"]
)


@router.get(
    "/",
    response_model=Page[NotificationResponse]
)
def get_notifications_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return paginate(
        db,
        get_notifications_statement(
            current_user
        )
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_notification_read_api(

    notification_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return mark_notification_read(
        db,
        notification_id,
        current_user
    )
