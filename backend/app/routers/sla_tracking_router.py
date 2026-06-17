from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    require_governance_viewer,
    require_manager_or_admin
)

from app.db.deps import get_db

from app.schemas.sla_schema import (
    SLATrackingResponse
)

from app.services.sla_service import (
    complete_sla_tracking,
    fetch_active_sla_tracking,
    fetch_breached_sla_tracking,
    fetch_completed_sla_tracking,
    fetch_sla_tracking_for_module,
    fetch_sla_tracking_for_record,
    start_approval_sla_tracking,
    start_task_sla_tracking
)


router = APIRouter(

    prefix="/sla-tracking",

    tags=["SLA Tracking"]
)


@router.post(
    "/tasks/{task_id}",
    response_model=SLATrackingResponse,
    status_code=201
)
def start_task_sla_tracking_api(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return start_task_sla_tracking(
        db,
        task_id,
        current_user
    )


@router.post(
    "/approvals/{approval_id}",
    response_model=SLATrackingResponse,
    status_code=201
)
def start_approval_sla_tracking_api(
    approval_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return start_approval_sla_tracking(
        db,
        approval_id,
        current_user
    )


@router.put(
    "/{tracking_id}/complete",
    response_model=SLATrackingResponse
)
def complete_sla_tracking_api(
    tracking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return complete_sla_tracking(
        db,
        tracking_id,
        current_user
    )


@router.get(
    "/active",
    response_model=list[SLATrackingResponse]
)
def get_active_sla_tracking_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return fetch_active_sla_tracking(
        db,
        current_user
    )


@router.get(
    "/breached",
    response_model=list[SLATrackingResponse]
)
def get_breached_sla_tracking_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return fetch_breached_sla_tracking(
        db,
        current_user
    )


@router.get(
    "/completed",
    response_model=list[SLATrackingResponse]
)
def get_completed_sla_tracking_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return fetch_completed_sla_tracking(
        db,
        current_user
    )


@router.get(
    "/module/{module_name}",
    response_model=list[SLATrackingResponse]
)
def get_sla_tracking_for_module_api(
    module_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return fetch_sla_tracking_for_module(
        db,
        module_name,
        current_user
    )


@router.get(
    "/record/{module_name}/{record_id}",
    response_model=SLATrackingResponse
)
def get_sla_tracking_for_record_api(
    module_name: str,
    record_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return fetch_sla_tracking_for_record(
        db,
        module_name,
        record_id,
        current_user
    )
