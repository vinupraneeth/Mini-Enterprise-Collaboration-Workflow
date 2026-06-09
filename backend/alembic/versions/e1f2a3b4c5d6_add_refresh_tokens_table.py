"""add refresh tokens table

Revision ID: e1f2a3b4c5d6
Revises: d6e7f8a9b0c1
Create Date: 2026-06-08
"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


revision: str = "e1f2a3b4c5d6"
down_revision: Union[str, Sequence[str], None] = "d6e7f8a9b0c1"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_refresh_tokens_id"),
        "refresh_tokens",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_refresh_tokens_token_hash"),
        "refresh_tokens",
        ["token_hash"],
        unique=True
    )

    op.create_index(
        op.f("ix_refresh_tokens_user_id"),
        "refresh_tokens",
        ["user_id"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f("ix_refresh_tokens_user_id"),
        table_name="refresh_tokens"
    )

    op.drop_index(
        op.f("ix_refresh_tokens_token_hash"),
        table_name="refresh_tokens"
    )

    op.drop_index(
        op.f("ix_refresh_tokens_id"),
        table_name="refresh_tokens"
    )

    op.drop_table("refresh_tokens")
