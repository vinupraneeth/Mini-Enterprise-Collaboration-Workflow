"""add phase8 workflow governance tables

Revision ID: e7f8a9b0c3d4
Revises: d6e7f8a9b0c2
Create Date: 2026-06-16
"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


revision: str = "e7f8a9b0c3d4"
down_revision: Union[str, Sequence[str], None] = "d6e7f8a9b0c2"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "tasks",
        sa.Column(
            "sla_status",
            sa.String(length=50),
            nullable=True
        )
    )

    op.add_column(
        "tasks",
        sa.Column(
            "sla_due_time",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.add_column(
        "tasks",
        sa.Column(
            "is_sla_breached",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.add_column(
        "approvals",
        sa.Column(
            "sla_status",
            sa.String(length=50),
            nullable=True
        )
    )

    op.add_column(
        "approvals",
        sa.Column(
            "sla_due_time",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.add_column(
        "approvals",
        sa.Column(
            "is_escalated",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.add_column(
        "approvals",
        sa.Column(
            "current_escalation_to",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_approvals_current_escalation_to_users",
        "approvals",
        "users",
        ["current_escalation_to"],
        ["id"]
    )

    op.add_column(
        "notifications",
        sa.Column(
            "notification_type",
            sa.String(length=50),
            nullable=True
        )
    )

    op.add_column(
        "notifications",
        sa.Column(
            "priority",
            sa.String(length=50),
            nullable=True
        )
    )

    op.add_column(
        "audit_logs",
        sa.Column(
            "module_name",
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        "audit_logs",
        sa.Column(
            "action_type",
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        "audit_logs",
        sa.Column(
            "record_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.add_column(
        "audit_logs",
        sa.Column(
            "old_data",
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        "audit_logs",
        sa.Column(
            "new_data",
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        "audit_logs",
        sa.Column(
            "ip_address",
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        "audit_logs",
        sa.Column(
            "user_agent",
            sa.String(length=500),
            nullable=True
        )
    )

    op.create_table(
        "sla_rules",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "module_name",
            sa.String(length=100),
            nullable=False
        ),
        sa.Column(
            "priority",
            sa.String(length=50),
            nullable=False
        ),
        sa.Column(
            "allowed_hours",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "escalation_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        ),
        sa.Column(
            "escalation_after_hours",
            sa.Integer(),
            nullable=True
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "created_by",
            sa.Integer(),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_sla_rules_id"),
        "sla_rules",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_sla_rules_is_active"),
        "sla_rules",
        ["is_active"],
        unique=False
    )

    op.create_index(
        op.f("ix_sla_rules_module_name"),
        "sla_rules",
        ["module_name"],
        unique=False
    )

    op.create_index(
        op.f("ix_sla_rules_priority"),
        "sla_rules",
        ["priority"],
        unique=False
    )

    op.create_table(
        "sla_tracking",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "module_name",
            sa.String(length=100),
            nullable=False
        ),
        sa.Column(
            "record_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "sla_rule_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "start_time",
            sa.DateTime(timezone=True),
            nullable=False
        ),
        sa.Column(
            "due_time",
            sa.DateTime(timezone=True),
            nullable=False
        ),
        sa.Column(
            "completed_time",
            sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False
        ),
        sa.Column(
            "breach_reason",
            sa.Text(),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["sla_rule_id"],
            ["sla_rules.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_sla_tracking_id"),
        "sla_tracking",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_sla_tracking_module_name"),
        "sla_tracking",
        ["module_name"],
        unique=False
    )

    op.create_index(
        op.f("ix_sla_tracking_record_id"),
        "sla_tracking",
        ["record_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_sla_tracking_status"),
        "sla_tracking",
        ["status"],
        unique=False
    )

    op.create_table(
        "approval_escalations",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "approval_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "escalated_from",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "escalated_to",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "reason",
            sa.Text(),
            nullable=False
        ),
        sa.Column(
            "escalation_level",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="pending"
        ),
        sa.Column(
            "escalated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.Column(
            "resolved_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["approval_id"],
            ["approvals.id"]
        ),
        sa.ForeignKeyConstraint(
            ["escalated_from"],
            ["users.id"]
        ),
        sa.ForeignKeyConstraint(
            ["escalated_to"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_approval_escalations_approval_id"),
        "approval_escalations",
        ["approval_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_approval_escalations_id"),
        "approval_escalations",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_approval_escalations_status"),
        "approval_escalations",
        ["status"],
        unique=False
    )

    op.create_table(
        "approval_delegations",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "delegator_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "delegatee_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "start_date",
            sa.DateTime(timezone=True),
            nullable=False
        ),
        sa.Column(
            "end_date",
            sa.DateTime(timezone=True),
            nullable=False
        ),
        sa.Column(
            "reason",
            sa.Text(),
            nullable=False
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["delegatee_id"],
            ["users.id"]
        ),
        sa.ForeignKeyConstraint(
            ["delegator_id"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_approval_delegations_delegatee_id"),
        "approval_delegations",
        ["delegatee_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_approval_delegations_delegator_id"),
        "approval_delegations",
        ["delegator_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_approval_delegations_id"),
        "approval_delegations",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_approval_delegations_is_active"),
        "approval_delegations",
        ["is_active"],
        unique=False
    )

    op.create_table(
        "notification_preferences",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "in_app_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "email_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        ),
        sa.Column(
            "task_notifications",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "approval_notifications",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "escalation_notifications",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "document_notifications",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id")
    )

    op.create_index(
        op.f("ix_notification_preferences_id"),
        "notification_preferences",
        ["id"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f("ix_notification_preferences_id"),
        table_name="notification_preferences"
    )

    op.drop_table("notification_preferences")

    op.drop_index(
        op.f("ix_approval_delegations_is_active"),
        table_name="approval_delegations"
    )

    op.drop_index(
        op.f("ix_approval_delegations_id"),
        table_name="approval_delegations"
    )

    op.drop_index(
        op.f("ix_approval_delegations_delegator_id"),
        table_name="approval_delegations"
    )

    op.drop_index(
        op.f("ix_approval_delegations_delegatee_id"),
        table_name="approval_delegations"
    )

    op.drop_table("approval_delegations")

    op.drop_index(
        op.f("ix_approval_escalations_status"),
        table_name="approval_escalations"
    )

    op.drop_index(
        op.f("ix_approval_escalations_id"),
        table_name="approval_escalations"
    )

    op.drop_index(
        op.f("ix_approval_escalations_approval_id"),
        table_name="approval_escalations"
    )

    op.drop_table("approval_escalations")

    op.drop_index(
        op.f("ix_sla_tracking_status"),
        table_name="sla_tracking"
    )

    op.drop_index(
        op.f("ix_sla_tracking_record_id"),
        table_name="sla_tracking"
    )

    op.drop_index(
        op.f("ix_sla_tracking_module_name"),
        table_name="sla_tracking"
    )

    op.drop_index(
        op.f("ix_sla_tracking_id"),
        table_name="sla_tracking"
    )

    op.drop_table("sla_tracking")

    op.drop_index(
        op.f("ix_sla_rules_priority"),
        table_name="sla_rules"
    )

    op.drop_index(
        op.f("ix_sla_rules_module_name"),
        table_name="sla_rules"
    )

    op.drop_index(
        op.f("ix_sla_rules_is_active"),
        table_name="sla_rules"
    )

    op.drop_index(
        op.f("ix_sla_rules_id"),
        table_name="sla_rules"
    )

    op.drop_table("sla_rules")

    op.drop_column(
        "audit_logs",
        "user_agent"
    )

    op.drop_column(
        "audit_logs",
        "ip_address"
    )

    op.drop_column(
        "audit_logs",
        "new_data"
    )

    op.drop_column(
        "audit_logs",
        "old_data"
    )

    op.drop_column(
        "audit_logs",
        "record_id"
    )

    op.drop_column(
        "audit_logs",
        "action_type"
    )

    op.drop_column(
        "audit_logs",
        "module_name"
    )

    op.drop_column(
        "notifications",
        "priority"
    )

    op.drop_column(
        "notifications",
        "notification_type"
    )

    op.drop_constraint(
        "fk_approvals_current_escalation_to_users",
        "approvals",
        type_="foreignkey"
    )

    op.drop_column(
        "approvals",
        "current_escalation_to"
    )

    op.drop_column(
        "approvals",
        "is_escalated"
    )

    op.drop_column(
        "approvals",
        "sla_due_time"
    )

    op.drop_column(
        "approvals",
        "sla_status"
    )

    op.drop_column(
        "tasks",
        "is_sla_breached"
    )

    op.drop_column(
        "tasks",
        "sla_due_time"
    )

    op.drop_column(
        "tasks",
        "sla_status"
    )
