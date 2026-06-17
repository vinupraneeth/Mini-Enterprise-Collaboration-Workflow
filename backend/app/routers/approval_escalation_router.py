from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    require_governance_viewer,
    require_manager_or_admin
)

from app.db.deps import get_db

from app.schemas.workflow_governance_schema import (
    ApprovalEscalationCreate,
    ApprovalEscalationResponse,
    ApprovalEscalationResolve
)

from app.services.workflow_governance_service import (
    cancel_approval_escalation,
    create_approval_escalation,
    get_approval_escalations_statement,
    get_escalation_history_statement,
    get_pending_approval_escalations_statement,
    resolve_approval_escalation
)


router = APIRouter(

    prefix="/approval-escalations",

    tags=["Approval Escalations"]
)


@router.post(
    "/",
    response_model=ApprovalEscalationResponse,
    status_code=201
)
def create_approval_escalation_api(
    escalation_data: ApprovalEscalationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return create_approval_escalation(
        db,
        escalation_data,
        current_user
    )


@router.get(
    "/",
    response_model=Page[ApprovalEscalationResponse]
)
def get_approval_escalations_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return paginate(
        db,
        get_approval_escalations_statement(
            current_user
        )
    )


@router.get(
    "/pending",
    response_model=Page[ApprovalEscalationResponse]
)
def get_pending_approval_escalations_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return paginate(
        db,
        get_pending_approval_escalations_statement(
            current_user
        )
    )


@router.get(
    "/approval/{approval_id}",
    response_model=Page[ApprovalEscalationResponse]
)
def get_approval_escalation_history_api(
    approval_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_governance_viewer)
):

    return paginate(
        db,
        get_escalation_history_statement(
            approval_id,
            current_user
        )
    )


@router.put(
    "/{escalation_id}/resolve",
    response_model=ApprovalEscalationResponse
)
def resolve_approval_escalation_api(
    escalation_id: int,
    resolve_data: ApprovalEscalationResolve,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return resolve_approval_escalation(
        db,
        escalation_id,
        current_user
    )


@router.put(
    "/{escalation_id}/cancel",
    response_model=ApprovalEscalationResponse
)
def cancel_approval_escalation_api(
    escalation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return cancel_approval_escalation(
        db,
        escalation_id,
        current_user
    )
