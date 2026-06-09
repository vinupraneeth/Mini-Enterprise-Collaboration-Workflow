from datetime import datetime

from typing import Literal

from pydantic import (
    BaseModel,
    Field
)


class OrganizationResponse(BaseModel):

    id: int

    name: str

    slug: str

    created_at: datetime | None = None

    class Config:

        from_attributes = True


class OrganizationCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150
    )

    slug: str = Field(
        min_length=1,
        max_length=120
    )


class SubscriptionPlanResponse(BaseModel):

    id: int

    name: str

    monthly_price: int

    monthly_credits: int

    max_users: int

    features: str | None = None

    class Config:

        from_attributes = True


class SubscriptionResponse(BaseModel):

    id: int

    organization_id: int

    plan_id: int

    status: str

    credits_remaining: int

    billing_provider: str | None = None

    provider_subscription_id: str | None = None

    created_at: datetime | None = None

    plan: SubscriptionPlanResponse | None = None

    class Config:

        from_attributes = True


class CreditLedgerResponse(BaseModel):

    id: int

    organization_id: int

    change_amount: int

    reason: str

    created_at: datetime | None = None

    class Config:

        from_attributes = True


class BillingTransactionResponse(BaseModel):

    id: int

    organization_id: int

    provider: str

    amount: int

    currency: str

    status: str

    provider_reference: str | None = None

    created_at: datetime | None = None

    class Config:

        from_attributes = True


class BillingRecordRequest(BaseModel):

    provider: Literal[
        "razorpay",
        "local"
    ] = "local"

    amount: int = Field(
        ge=0
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=10
    )

    provider_reference: str | None = Field(
        default=None,
        max_length=150
    )
