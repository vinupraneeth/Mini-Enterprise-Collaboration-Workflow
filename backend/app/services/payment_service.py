import importlib

from fastapi import HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.core.config import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET
)

from app.models.saas_model import (
    BillingTransaction,
    CreditLedger,
    Subscription
)

from app.services.saas_service import (
    get_current_organization,
    get_current_subscription,
    get_plan_by_name
)


def get_razorpay_client():

    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:

        raise HTTPException(
            status_code=503,
            detail="Razorpay credentials are not configured"
        )

    razorpay_module = importlib.import_module(
        "razorpay"
    )

    return razorpay_module.Client(
        auth=(
            RAZORPAY_KEY_ID,
            RAZORPAY_KEY_SECRET
        )
    )


def get_plan_amount_paise(
    plan
):

    return plan.monthly_price * 100


def create_razorpay_order(
    db: Session,
    current_user,
    plan_name: str
):

    plan = get_plan_by_name(
        db,
        plan_name
    )

    if plan.monthly_price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Free Basic plan does not require Razorpay payment"
        )

    try:

        client = get_razorpay_client()

    except ModuleNotFoundError:

        raise HTTPException(
            status_code=503,
            detail="Razorpay package is not installed"
        )

    order = client.order.create(
        {
            "amount": get_plan_amount_paise(
                plan
            ),
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "plan": plan.name,
                "organization_id": str(
                    current_user.organization_id
                )
            }
        }
    )

    return {
        "provider": "razorpay",
        "key": RAZORPAY_KEY_ID,
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "plan_name": plan.name,
        "credits": plan.monthly_credits
    }


def verify_razorpay_payment(
    db: Session,
    current_user,
    payment_data
):

    organization = get_current_organization(
        db,
        current_user
    )

    plan = get_plan_by_name(
        db,
        payment_data.plan_name
    )

    existing_payment = db.execute(
        select(Subscription).where(
            Subscription.razorpay_payment_id ==
            payment_data.razorpay_payment_id
        )
    ).scalar_one_or_none()

    if existing_payment:

        raise HTTPException(
            status_code=400,
            detail="Payment already processed"
        )

    try:

        client = get_razorpay_client()

    except ModuleNotFoundError:

        raise HTTPException(
            status_code=503,
            detail="Razorpay package is not installed"
        )

    try:

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id":
                    payment_data.razorpay_order_id,
                "razorpay_payment_id":
                    payment_data.razorpay_payment_id,
                "razorpay_signature":
                    payment_data.razorpay_signature
            }
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid Razorpay payment signature"
        )

    subscription = activate_paid_subscription(
        db,
        current_user,
        organization,
        plan,
        "razorpay",
        payment_data.razorpay_order_id,
        payment_data.razorpay_payment_id,
        payment_data.razorpay_signature,
        f"{plan.name} plan credits added through Razorpay"
    )

    return {
        "message": "Razorpay payment verified and subscription activated",
        "subscription": subscription
    }


def activate_paid_subscription(
    db: Session,
    current_user,
    organization,
    plan,
    provider,
    order_id,
    payment_id,
    signature,
    credit_reason
):

    subscription = get_current_subscription(
        db,
        current_user
    )

    subscription.plan_id = plan.id

    subscription.status = "active"

    subscription.credits_remaining = (
        subscription.credits_remaining
        + plan.monthly_credits
    )

    subscription.billing_provider = provider

    subscription.provider_subscription_id = order_id

    subscription.razorpay_order_id = order_id

    subscription.razorpay_payment_id = payment_id

    subscription.razorpay_signature = signature

    db.add(
        CreditLedger(
            organization_id=organization.id,
            change_amount=plan.monthly_credits,
            reason=credit_reason
        )
    )

    db.add(
        BillingTransaction(
            organization_id=organization.id,
            provider=provider,
            amount=plan.monthly_price,
            currency="INR",
            status="success",
            provider_reference=payment_id
        )
    )

    db.commit()

    db.refresh(subscription)

    return subscription

