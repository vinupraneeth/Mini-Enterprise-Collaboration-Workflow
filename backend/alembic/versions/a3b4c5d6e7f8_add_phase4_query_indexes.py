"""add phase 4 query indexes

Revision ID: a3b4c5d6e7f8
Revises: f2a3b4c5d6e7
Create Date: 2026-06-08
"""

from typing import Sequence, Union

from alembic import op


revision: str = "a3b4c5d6e7f8"
down_revision: Union[str, Sequence[str], None] = "f2a3b4c5d6e7"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_index(
        "ix_tasks_status",
        "tasks",
        ["status"],
        unique=False
    )

    op.create_index(
        "ix_tasks_priority",
        "tasks",
        ["priority"],
        unique=False
    )

    op.create_index(
        "ix_tasks_assigned_to",
        "tasks",
        ["assigned_to"],
        unique=False
    )

    op.create_index(
        "ix_tasks_created_by",
        "tasks",
        ["created_by"],
        unique=False
    )

    op.create_index(
        "ix_tasks_due_date",
        "tasks",
        ["due_date"],
        unique=False
    )

    op.create_index(
        "ix_approvals_status",
        "approvals",
        ["status"],
        unique=False
    )

    op.create_index(
        "ix_approvals_current_level",
        "approvals",
        ["current_level"],
        unique=False
    )

    op.create_index(
        "ix_approvals_requested_by",
        "approvals",
        ["requested_by"],
        unique=False
    )

    op.create_index(
        "ix_approvals_task_id",
        "approvals",
        ["task_id"],
        unique=False
    )

    op.create_index(
        "ix_notifications_user_read",
        "notifications",
        ["user_id", "is_read"],
        unique=False
    )

    op.create_index(
        "ix_documents_task_id",
        "documents",
        ["task_id"],
        unique=False
    )

    op.create_index(
        "ix_documents_uploaded_by",
        "documents",
        ["uploaded_by"],
        unique=False
    )

    op.create_index(
        "ix_audit_logs_user_id",
        "audit_logs",
        ["user_id"],
        unique=False
    )

    op.create_index(
        "ix_audit_logs_entity",
        "audit_logs",
        ["entity", "entity_id"],
        unique=False
    )

    op.create_index(
        "ix_audit_logs_timestamp",
        "audit_logs",
        ["timestamp"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        "ix_audit_logs_timestamp",
        table_name="audit_logs"
    )

    op.drop_index(
        "ix_audit_logs_entity",
        table_name="audit_logs"
    )

    op.drop_index(
        "ix_audit_logs_user_id",
        table_name="audit_logs"
    )

    op.drop_index(
        "ix_documents_uploaded_by",
        table_name="documents"
    )

    op.drop_index(
        "ix_documents_task_id",
        table_name="documents"
    )

    op.drop_index(
        "ix_notifications_user_read",
        table_name="notifications"
    )

    op.drop_index(
        "ix_approvals_task_id",
        table_name="approvals"
    )

    op.drop_index(
        "ix_approvals_requested_by",
        table_name="approvals"
    )

    op.drop_index(
        "ix_approvals_current_level",
        table_name="approvals"
    )

    op.drop_index(
        "ix_approvals_status",
        table_name="approvals"
    )

    op.drop_index(
        "ix_tasks_due_date",
        table_name="tasks"
    )

    op.drop_index(
        "ix_tasks_created_by",
        table_name="tasks"
    )

    op.drop_index(
        "ix_tasks_assigned_to",
        table_name="tasks"
    )

    op.drop_index(
        "ix_tasks_priority",
        table_name="tasks"
    )

    op.drop_index(
        "ix_tasks_status",
        table_name="tasks"
    )
