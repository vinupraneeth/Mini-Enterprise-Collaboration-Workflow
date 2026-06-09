"""add phase 7 saas tables

Revision ID: b4c5d6e7f8a9
Revises: a3b4c5d6e7f8
Create Date: 2026-06-09
"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


revision: str = "b4c5d6e7f8a9"
down_revision: Union[str, Sequence[str], None] = "a3b4c5d6e7f8"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug")
    )

    op.create_index(
        "ix_organizations_id",
        "organizations",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_organizations_slug",
        "organizations",
        ["slug"],
        unique=False
    )

    op.create_table(
        "subscription_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("monthly_price", sa.Integer(), nullable=False),
        sa.Column("monthly_credits", sa.Integer(), nullable=False),
        sa.Column("max_users", sa.Integer(), nullable=False),
        sa.Column("features", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name")
    )

    op.create_index(
        "ix_subscription_plans_id",
        "subscription_plans",
        ["id"],
        unique=False
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("plan_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("credits_remaining", sa.Integer(), nullable=True),
        sa.Column("billing_provider", sa.String(length=50), nullable=True),
        sa.Column("provider_subscription_id", sa.String(length=150), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["plan_id"], ["subscription_plans.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_subscriptions_id",
        "subscriptions",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_subscriptions_organization_id",
        "subscriptions",
        ["organization_id"],
        unique=False
    )

    op.create_table(
        "credit_ledger",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("change_amount", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_credit_ledger_id",
        "credit_ledger",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_credit_ledger_organization_id",
        "credit_ledger",
        ["organization_id"],
        unique=False
    )

    op.create_table(
        "billing_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("provider_reference", sa.String(length=150), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_billing_transactions_id",
        "billing_transactions",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_billing_transactions_organization_id",
        "billing_transactions",
        ["organization_id"],
        unique=False
    )

    op.add_column(
        "users",
        sa.Column("organization_id", sa.Integer(), nullable=True)
    )

    op.create_index(
        "ix_users_organization_id",
        "users",
        ["organization_id"],
        unique=False
    )

    op.create_foreign_key(
        "fk_users_organization_id",
        "users",
        "organizations",
        ["organization_id"],
        ["id"]
    )

    op.execute(
        "INSERT INTO organizations (id, name, slug) VALUES "
        "(1, 'Default Organization', 'default-organization')"
    )

    op.execute(
        "UPDATE users SET organization_id = 1 WHERE organization_id IS NULL"
    )

    op.execute(
        "INSERT INTO subscription_plans "
        "(id, name, monthly_price, monthly_credits, max_users, features) VALUES "
        "(1, 'Basic', 0, 100, 10, 'Core workflow, tasks, approvals'), "
        "(2, 'Silver', 999, 500, 50, 'Core workflow, analytics, priority support'), "
        "(3, 'Gold', 2499, 1500, 200, 'Full enterprise workflow, analytics, billing support')"
    )

    op.execute(
        "INSERT INTO subscriptions "
        "(organization_id, plan_id, status, credits_remaining, billing_provider) VALUES "
        "(1, 1, 'active', 100, 'local')"
    )

    op.execute(
        "INSERT INTO credit_ledger "
        "(organization_id, change_amount, reason) VALUES "
        "(1, 100, 'Initial Basic plan credits')"
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_users_organization_id",
        "users",
        type_="foreignkey"
    )

    op.drop_index(
        "ix_users_organization_id",
        table_name="users"
    )

    op.drop_column(
        "users",
        "organization_id"
    )

    op.drop_index(
        "ix_billing_transactions_organization_id",
        table_name="billing_transactions"
    )

    op.drop_index(
        "ix_billing_transactions_id",
        table_name="billing_transactions"
    )

    op.drop_table("billing_transactions")

    op.drop_index(
        "ix_credit_ledger_organization_id",
        table_name="credit_ledger"
    )

    op.drop_index(
        "ix_credit_ledger_id",
        table_name="credit_ledger"
    )

    op.drop_table("credit_ledger")

    op.drop_index(
        "ix_subscriptions_organization_id",
        table_name="subscriptions"
    )

    op.drop_index(
        "ix_subscriptions_id",
        table_name="subscriptions"
    )

    op.drop_table("subscriptions")

    op.drop_index(
        "ix_subscription_plans_id",
        table_name="subscription_plans"
    )

    op.drop_table("subscription_plans")

    op.drop_index(
        "ix_organizations_slug",
        table_name="organizations"
    )

    op.drop_index(
        "ix_organizations_id",
        table_name="organizations"
    )

    op.drop_table("organizations")
