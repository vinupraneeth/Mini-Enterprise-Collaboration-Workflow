"""add approval level and history comment

Revision ID: b2f6c1d47a25
Revises: f0d3420547f8
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2f6c1d47a25'
down_revision: Union[str, Sequence[str], None] = 'f0d3420547f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'approvals',
        sa.Column(
            'current_level',
            sa.String(length=50),
            nullable=True,
            server_default='manager'
        )
    )

    op.add_column(
        'approval_history',
        sa.Column(
            'comment',
            sa.Text(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'approval_history',
        'comment'
    )

    op.drop_column(
        'approvals',
        'current_level'
    )
