"""update subscription plan catalog

Revision ID: d6e7f8a9b0c2
Revises: c5d6e7f8a9b0
Create Date: 2026-06-09
"""

from typing import Sequence, Union

from alembic import op


revision: str = "d6e7f8a9b0c2"
down_revision: Union[str, Sequence[str], None] = "c5d6e7f8a9b0"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute(
        "UPDATE subscription_plans SET "
        "monthly_price = 499, "
        "monthly_credits = 300, "
        "max_users = 10, "
        "features = 'Task and Kanban workflow;Role-based access control;In-app notifications;Document upload and versioning;AI workflow summary;300 monthly credits' "
        "WHERE name = 'Basic'"
    )

    op.execute(
        "UPDATE subscription_plans SET "
        "monthly_price = 1499, "
        "monthly_credits = 1000, "
        "max_users = 50, "
        "features = 'Everything in Basic;Approval workflow and audit logs;Live notifications and Kanban updates;Role dashboards for teams;Smart assignment recommendations;1000 monthly credits' "
        "WHERE name = 'Silver'"
    )

    op.execute(
        "UPDATE subscription_plans SET "
        "monthly_price = 3999, "
        "monthly_credits = 3000, "
        "max_users = 200, "
        "features = 'Everything in Silver;Multi-organization SaaS management;Advanced audit and activity tracking;Priority workflow monitoring;Enterprise document governance;3000 monthly credits' "
        "WHERE name = 'Gold'"
    )

    op.execute(
        "UPDATE subscriptions "
        "SET credits_remaining = 300 "
        "WHERE plan_id = 1 AND credits_remaining < 300"
    )


def downgrade() -> None:

    op.execute(
        "UPDATE subscription_plans SET "
        "monthly_price = 0, "
        "monthly_credits = 100, "
        "max_users = 10, "
        "features = 'Core workflow, tasks, approvals' "
        "WHERE name = 'Basic'"
    )

    op.execute(
        "UPDATE subscription_plans SET "
        "monthly_price = 999, "
        "monthly_credits = 500, "
        "max_users = 50, "
        "features = 'Core workflow, analytics, priority support' "
        "WHERE name = 'Silver'"
    )

    op.execute(
        "UPDATE subscription_plans SET "
        "monthly_price = 2499, "
        "monthly_credits = 1500, "
        "max_users = 200, "
        "features = 'Full enterprise workflow, analytics, billing support' "
        "WHERE name = 'Gold'"
    )
