"""align phase 2 approval workflow

Revision ID: c9f1a2b3d4e5
Revises: b2f6c1d47a25
Create Date: 2026-05-28
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "c9f1a2b3d4e5"
down_revision: Union[str, Sequence[str], None] = "b2f6c1d47a25"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()))
    op.add_column("users", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True))
    op.add_column("users", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True))

    op.add_column("approvals", sa.Column("title", sa.String(length=255), nullable=True))
    op.add_column("approvals", sa.Column("description", sa.Text(), nullable=True))
    op.alter_column("approvals", "task_id", existing_type=sa.Integer(), nullable=True)

    op.add_column("approval_history", sa.Column("action_by", sa.Integer(), nullable=True))
    op.add_column("approval_history", sa.Column("action", sa.String(length=50), nullable=True))
    op.create_foreign_key("fk_approval_history_action_by_users", "approval_history", "users", ["action_by"], ["id"])

    op.execute("UPDATE approvals SET title = 'Task approval request' WHERE title IS NULL")
    op.alter_column("approvals", "title", existing_type=sa.String(length=255), nullable=False)


def downgrade() -> None:
    op.drop_constraint("fk_approval_history_action_by_users", "approval_history", type_="foreignkey")
    op.drop_column("approval_history", "action")
    op.drop_column("approval_history", "action_by")

    op.alter_column("approvals", "task_id", existing_type=sa.Integer(), nullable=False)
    op.drop_column("approvals", "description")
    op.drop_column("approvals", "title")

    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    op.drop_column("users", "is_active")