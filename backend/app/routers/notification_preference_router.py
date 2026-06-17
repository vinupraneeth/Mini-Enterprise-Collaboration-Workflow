from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    require_admin
)

from app.db.deps import get_db

from app.schemas.workflow_governance_schema import (
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate
)

from app.services.workflow_governance_service import (
    create_default_notification_preferences,
    get_my_notification_preferences,
    update_my_notification_preferences
)


router = APIRouter(

    prefix="/notification-preferences",

    tags=["Notification Preferences"]
)


@router.get(
    "/me",
    response_model=NotificationPreferenceResponse
)
def get_my_notification_preferences_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_my_notification_preferences(
        db,
        current_user
    )


@router.put(
    "/me",
    response_model=NotificationPreferenceResponse
)
def update_my_notification_preferences_api(
    preference_data: NotificationPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return update_my_notification_preferences(
        db,
        preference_data,
        current_user
    )


@router.post(
    "/default/{user_id}",
    response_model=NotificationPreferenceResponse,
    status_code=201
)
def create_default_notification_preferences_api(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_default_notification_preferences(
        db,
        user_id,
        current_user
    )
