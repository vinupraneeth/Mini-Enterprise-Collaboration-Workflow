"""add razorpay subscription fields

Revision ID: c5d6e7f8a9b0
Revises: b4c5d6e7f8a9
Create Date: 2026-06-09
"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


revision: str = "c5d6e7f8a9b0"
down_revision: Union[str, Sequence[str], None] = "b4c5d6e7f8a9"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "subscriptions",
        sa.Column(
            "razorpay_order_id",
            sa.String(length=150),
            nullable=True
        )
    )

    op.add_column(
        "subscriptions",
        sa.Column(
            "razorpay_payment_id",
            sa.String(length=150),
            nullable=True
        )
    )

    op.add_column(
        "subscriptions",
        sa.Column(
            "razorpay_signature",
            sa.String(length=255),
            nullable=True
        )
    )

    op.create_index(
        "ix_subscriptions_razorpay_order_id",
        "subscriptions",
        ["razorpay_order_id"],
        unique=False
    )

    op.create_index(
        "ix_subscriptions_razorpay_payment_id",
        "subscriptions",
        ["razorpay_payment_id"],
        unique=True
    )


def downgrade() -> None:

    op.drop_index(
        "ix_subscriptions_razorpay_payment_id",
        table_name="subscriptions"
    )

    op.drop_index(
        "ix_subscriptions_razorpay_order_id",
        table_name="subscriptions"
    )

    op.drop_column(
        "subscriptions",
        "razorpay_signature"
    )

    op.drop_column(
        "subscriptions",
        "razorpay_payment_id"
    )

    op.drop_column(
        "subscriptions",
        "razorpay_order_id"
    )
