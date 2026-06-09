from fastapi import HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.models.saas_model import (
    BillingTransaction,
    CreditLedger,
    Organization,
    Subscription,
    SubscriptionPlan
)


DEFAULT_ORGANIZATION_NAME = "Default Organization"

DEFAULT_ORGANIZATION_SLUG = "default-organization"


def get_default_organization(
    db: Session
):

    organization = db.execute(
        select(Organization).where(
            Organization.slug == DEFAULT_ORGANIZATION_SLUG
        )
    ).scalar_one_or_none()

    if organization:

        return organization

    organization = Organization(
        name=DEFAULT_ORGANIZATION_NAME,
        slug=DEFAULT_ORGANIZATION_SLUG
    )

    db.add(organization)

    db.flush()

    return organization


def get_current_organization(
    db: Session,
    current_user
):

    if current_user.organization_id:

        organization = db.execute(
            select(Organization).where(
                Organization.id == current_user.organization_id
            )
        ).scalar_one_or_none()

        if organization:

            return organization

    organization = get_default_organization(
        db
    )

    current_user.organization_id = organization.id

    db.commit()

    return organization


def create_organization(
    db: Session,
    organization_data
):

    existing_organization = db.execute(
        select(Organization).where(
            Organization.slug == organization_data.slug
        )
    ).scalar_one_or_none()

    if existing_organization:

        raise HTTPException(
            status_code=400,
            detail="Organization slug already exists"
        )

    organization = Organization(
        name=organization_data.name,
        slug=organization_data.slug
    )

    db.add(organization)

    db.commit()

    db.refresh(organization)

    return organization


def get_organizations(
    db: Session
):

    return db.execute(
        select(Organization).order_by(
            Organization.created_at.desc()
        )
    ).scalars().all()


def get_subscription_plans(
    db: Session
):

    return db.execute(
        select(SubscriptionPlan).order_by(
            SubscriptionPlan.monthly_price
        )
    ).scalars().all()


def get_plan_by_name(
    db: Session,
    plan_name: str
):

    plan = db.execute(
        select(SubscriptionPlan).where(
            SubscriptionPlan.name == plan_name
        )
    ).scalar_one_or_none()

    if not plan:

        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found"
        )

    return plan


def get_current_subscription(
    db: Session,
    current_user
):

    organization = get_current_organization(
        db,
        current_user
    )

    subscription = db.execute(
        select(Subscription).where(
            Subscription.organization_id == organization.id
        ).order_by(
            Subscription.id.desc()
        )
    ).scalar_one_or_none()

    if subscription:

        return subscription

    plan = get_plan_by_name(
        db,
        "Basic"
    )

    subscription = Subscription(
        organization_id=organization.id,
        plan_id=plan.id,
        status="active",
        credits_remaining=plan.monthly_credits,
        billing_provider="local"
    )

    db.add(subscription)

    db.add(
        CreditLedger(
            organization_id=organization.id,
            change_amount=plan.monthly_credits,
            reason="Initial Basic plan credits"
        )
    )

    db.commit()

    db.refresh(subscription)

    return subscription


def get_credit_history(
    db: Session,
    current_user
):

    organization = get_current_organization(
        db,
        current_user
    )

    return db.execute(
        select(CreditLedger).where(
            CreditLedger.organization_id == organization.id
        ).order_by(
            CreditLedger.created_at.desc()
        )
    ).scalars().all()


def record_billing_transaction(
    db: Session,
    current_user,
    billing_data
):

    organization = get_current_organization(
        db,
        current_user
    )

    transaction = BillingTransaction(
        organization_id=organization.id,
        provider=billing_data.provider,
        amount=billing_data.amount,
        currency=billing_data.currency.upper(),
        status="success",
        provider_reference=billing_data.provider_reference
    )

    db.add(transaction)

    db.commit()

    db.refresh(transaction)

    return transaction
