from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Organization(Base):

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    slug: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
        index=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    users = relationship(
        "User",
        back_populates="organization"
    )


class SubscriptionPlan(Base):

    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    monthly_price: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    monthly_credits: Mapped[int] = mapped_column(
        Integer,
        default=100
    )

    max_users: Mapped[int] = mapped_column(
        Integer,
        default=10
    )

    features: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


class Subscription(Base):

    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("subscription_plans.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active"
    )

    credits_remaining: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    billing_provider: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    provider_subscription_id: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    razorpay_order_id: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    razorpay_payment_id: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    razorpay_signature: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    organization = relationship("Organization")
    plan = relationship("SubscriptionPlan")


class CreditLedger(Base):

    __tablename__ = "credit_ledger"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    change_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class BillingTransaction(Base):

    __tablename__ = "billing_transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR"
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="created"
    )

    provider_reference: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
