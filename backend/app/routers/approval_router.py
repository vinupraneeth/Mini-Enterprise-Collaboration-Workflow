from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.core.dependencies import (
    get_current_user
)

from app.schemas.approval_schema import (

    ApprovalCreate,

    ApprovalReview,

    ApprovalResponse,

    ApprovalHistoryResponse
)

from app.services.approval_service import (

    create_approval_request,

    fetch_approvals,

    review_approval_request,

    fetch_approval_history
)


router = APIRouter(

    prefix="/approvals",

    tags=["Approvals"]
)


@router.post(

    "/",

    response_model=ApprovalResponse,

    status_code=201
)
def create_approval_api(

    approval_data: ApprovalCreate,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return create_approval_request(

        db,

        approval_data,

        current_user
    )


@router.get(

    "/",

    response_model=list[
        ApprovalResponse
    ]
)
def get_approvals_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return fetch_approvals(

    db,

    current_user
    )


@router.patch(

    "/{approval_id}/action",

    response_model=ApprovalResponse
)
def approval_action_api(

    approval_id: int,

    review_data: ApprovalReview,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return review_approval_request(

        db,

        approval_id,

        review_data,

        current_user
    )


@router.get(
    "/{approval_id}/history",

    response_model=list[ApprovalHistoryResponse]
)
def get_approval_history_api(

    approval_id: int,
    db: Session = Depends(get_db),
    
    current_user = Depends(get_current_user)
):

    return fetch_approval_history(

        db,

        approval_id,

        current_user
    )


@router.patch(

    "/{approval_id}",

    response_model=ApprovalResponse
)
def review_approval_api(

    approval_id: int,

    review_data: ApprovalReview,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return review_approval_request(

        db,

        approval_id,

        review_data,

        current_user
    )
