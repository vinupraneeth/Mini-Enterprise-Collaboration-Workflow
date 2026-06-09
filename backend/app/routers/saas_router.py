from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    require_admin
)

from app.db.deps import get_db

from app.models.saas_model import (
    BillingTransaction,
    Organization
)

from app.schemas.saas_schema import (
    BillingRecordRequest,
    BillingTransactionResponse,
    CreditLedgerResponse,
    OrganizationCreate,
    OrganizationResponse,
    SubscriptionPlanResponse,
    SubscriptionResponse
)

from app.services.saas_service import (
    create_organization,
    get_credit_history,
    get_current_organization,
    get_current_subscription,
    get_subscription_plans,
    record_billing_transaction
)


router = APIRouter(
    prefix="/saas",
    tags=["SaaS"]
)


@router.get(
    "/organizations",
    response_model=Page[OrganizationResponse]
)
def get_organizations_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return paginate(
        db,
        select(Organization).order_by(
            Organization.created_at.desc()
        )
    )


@router.post(
    "/organizations",
    response_model=OrganizationResponse,
    status_code=201
)
def create_organization_api(
    organization_data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_organization(
        db,
        organization_data
    )


@router.get(
    "/organization",
    response_model=OrganizationResponse
)
def get_organization_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_current_organization(
        db,
        current_user
    )


@router.get(
    "/plans",
    response_model=list[SubscriptionPlanResponse]
)
def get_plans_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_subscription_plans(
        db
    )


@router.get(
    "/subscription",
    response_model=SubscriptionResponse
)
def get_subscription_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_current_subscription(
        db,
        current_user
    )


@router.get(
    "/credits",
    response_model=list[CreditLedgerResponse]
)
def get_credits_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_credit_history(
        db,
        current_user
    )


@router.post(
    "/billing/record",
    response_model=BillingTransactionResponse,
    status_code=201
)
def record_billing_api(
    billing_data: BillingRecordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return record_billing_transaction(
        db,
        current_user,
        billing_data
    )


@router.get(
    "/billing/transactions",
    response_model=Page[BillingTransactionResponse]
)
def get_billing_transactions_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return paginate(
        db,
        select(BillingTransaction).where(
            BillingTransaction.organization_id ==
            current_user.organization_id
        ).order_by(
            BillingTransaction.created_at.desc()
        )
    )
