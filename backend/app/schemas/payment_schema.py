from typing import Literal

from pydantic import (
    BaseModel,
    Field
)


class PaymentCreateRequest(BaseModel):

    plan_name: Literal[
        "Basic",
        "Silver",
        "Gold"
    ]

    provider: Literal[
        "razorpay"
    ] = "razorpay"


class RazorpayVerifyRequest(BaseModel):

    razorpay_order_id: str = Field(
        min_length=1,
        max_length=150
    )

    razorpay_payment_id: str = Field(
        min_length=1,
        max_length=150
    )

    razorpay_signature: str = Field(
        min_length=1,
        max_length=255
    )

    plan_name: Literal[
        "Basic",
        "Silver",
        "Gold"
    ]

