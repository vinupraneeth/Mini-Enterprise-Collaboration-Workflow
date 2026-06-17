from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    require_manager_or_admin
)

from app.db.deps import get_db

from app.schemas.workflow_governance_schema import (
    ApprovalDelegationCreate,
    ApprovalDelegationResponse
)

from app.services.workflow_governance_service import (
    cancel_approval_delegation,
    create_approval_delegation,
    get_active_delegations_statement,
    get_my_delegations_statement
)


router = APIRouter(

    prefix="/approval-delegations",

    tags=["Approval Delegations"]
)


@router.post(
    "/",
    response_model=ApprovalDelegationResponse,
    status_code=201
)
def create_approval_delegation_api(
    delegation_data: ApprovalDelegationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return create_approval_delegation(
        db,
        delegation_data,
        current_user
    )


@router.get(
    "/me",
    response_model=Page[ApprovalDelegationResponse]
)
def get_my_approval_delegations_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return paginate(
        db,
        get_my_delegations_statement(
            current_user
        )
    )


@router.get(
    "/active",
    response_model=Page[ApprovalDelegationResponse]
)
def get_active_approval_delegations_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return paginate(
        db,
        get_active_delegations_statement(
            db,
            current_user
        )
    )


@router.put(
    "/{delegation_id}/cancel",
    response_model=ApprovalDelegationResponse
)
def cancel_approval_delegation_api(
    delegation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_or_admin)
):

    return cancel_approval_delegation(
        db,
        delegation_id,
        current_user
    )
