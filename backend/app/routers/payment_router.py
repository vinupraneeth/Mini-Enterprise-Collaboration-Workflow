from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    require_admin
)

from app.db.deps import get_db

from app.schemas.payment_schema import (
    PaymentCreateRequest,
    RazorpayVerifyRequest
)

from app.services.payment_service import (
    create_razorpay_order,
    verify_razorpay_payment
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/create-payment"
)
def create_payment_api(
    payment_data: PaymentCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_razorpay_order(
        db,
        current_user,
        payment_data.plan_name
    )


@router.post(
    "/verify-razorpay"
)
def verify_razorpay_api(
    payment_data: RazorpayVerifyRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return verify_razorpay_payment(
        db,
        current_user,
        payment_data
    )

