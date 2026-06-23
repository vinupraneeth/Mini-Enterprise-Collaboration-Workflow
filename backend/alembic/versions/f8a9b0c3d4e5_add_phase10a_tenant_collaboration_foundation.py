"""add phase10a tenant collaboration foundation

Revision ID: f8a9b0c3d4e5
Revises: e7f8a9b0c3d4
Create Date: 2026-06-22
"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


revision: str = "f8a9b0c3d4e5"
down_revision: Union[str, Sequence[str], None] = "e7f8a9b0c3d4"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "organizations",
        sa.Column(
            "contact_email",
            sa.String(length=255),
            nullable=True
        )
    )

    op.add_column(
        "organizations",
        sa.Column(
            "phone",
            sa.String(length=30),
            nullable=True
        )
    )

    op.add_column(
        "organizations",
        sa.Column(
            "address",
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        "organizations",
        sa.Column(
            "industry",
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        "organizations",
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="ACTIVE"
        )
    )

    op.add_column(
        "organizations",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        )
    )

    op.create_index(
        op.f("ix_organizations_contact_email"),
        "organizations",
        ["contact_email"],
        unique=True
    )

    op.create_index(
        op.f("ix_organizations_status"),
        "organizations",
        ["status"],
        unique=False
    )

    op.create_table(
        "tenant_onboarding",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "admin_user_id",
            sa.Integer(),
            nullable=True
        ),
        sa.Column(
            "onboarding_status",
            sa.String(length=50),
            nullable=False,
            server_default="PENDING"
        ),
        sa.Column(
            "default_workspace_created",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        ),
        sa.Column(
            "settings_created",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        ),
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["admin_user_id"],
            ["users.id"]
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["organizations.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id")
    )

    op.create_index(
        op.f("ix_tenant_onboarding_admin_user_id"),
        "tenant_onboarding",
        ["admin_user_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_tenant_onboarding_id"),
        "tenant_onboarding",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_tenant_onboarding_onboarding_status"),
        "tenant_onboarding",
        ["onboarding_status"],
        unique=False
    )

    op.create_index(
        op.f("ix_tenant_onboarding_tenant_id"),
        "tenant_onboarding",
        ["tenant_id"],
        unique=True
    )

    op.create_table(
        "tenant_collaboration_settings",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "max_workspaces",
            sa.Integer(),
            nullable=False,
            server_default="5"
        ),
        sa.Column(
            "max_channels_per_workspace",
            sa.Integer(),
            nullable=False,
            server_default="10"
        ),
        sa.Column(
            "max_workspace_members",
            sa.Integer(),
            nullable=False,
            server_default="50"
        ),
        sa.Column(
            "max_storage_mb",
            sa.Integer(),
            nullable=False,
            server_default="1024"
        ),
        sa.Column(
            "workspace_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "channel_enabled",
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
            ["tenant_id"],
            ["organizations.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id")
    )

    op.create_index(
        op.f("ix_tenant_collaboration_settings_id"),
        "tenant_collaboration_settings",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_tenant_collaboration_settings_tenant_id"),
        "tenant_collaboration_settings",
        ["tenant_id"],
        unique=True
    )

    op.create_table(
        "tenant_collaboration_usage",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "workspace_count",
            sa.Integer(),
            nullable=False,
            server_default="0"
        ),
        sa.Column(
            "channel_count",
            sa.Integer(),
            nullable=False,
            server_default="0"
        ),
        sa.Column(
            "member_count",
            sa.Integer(),
            nullable=False,
            server_default="0"
        ),
        sa.Column(
            "storage_used_mb",
            sa.Integer(),
            nullable=False,
            server_default="0"
        ),
        sa.Column(
            "last_calculated_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["organizations.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id")
    )

    op.create_index(
        op.f("ix_tenant_collaboration_usage_id"),
        "tenant_collaboration_usage",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_tenant_collaboration_usage_tenant_id"),
        "tenant_collaboration_usage",
        ["tenant_id"],
        unique=True
    )

    op.create_table(
        "workspaces",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False
        ),
        sa.Column(
            "slug",
            sa.String(length=150),
            nullable=False
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True
        ),
        sa.Column(
            "avatar_url",
            sa.String(length=500),
            nullable=True
        ),
        sa.Column(
            "visibility",
            sa.String(length=50),
            nullable=False,
            server_default="PUBLIC"
        ),
        sa.Column(
            "created_by",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "is_archived",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
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
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["organizations.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "slug",
            name="uq_workspaces_tenant_slug"
        )
    )

    op.create_index(
        op.f("ix_workspaces_created_by"),
        "workspaces",
        ["created_by"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspaces_id"),
        "workspaces",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspaces_is_archived"),
        "workspaces",
        ["is_archived"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspaces_slug"),
        "workspaces",
        ["slug"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspaces_tenant_id"),
        "workspaces",
        ["tenant_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspaces_visibility"),
        "workspaces",
        ["visibility"],
        unique=False
    )

    op.create_table(
        "workspace_members",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "workspace_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="MEMBER"
        ),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workspace_id",
            "user_id",
            name="uq_workspace_members_workspace_user"
        )
    )

    op.create_index(
        op.f("ix_workspace_members_id"),
        "workspace_members",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspace_members_is_active"),
        "workspace_members",
        ["is_active"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspace_members_role"),
        "workspace_members",
        ["role"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspace_members_user_id"),
        "workspace_members",
        ["user_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_workspace_members_workspace_id"),
        "workspace_members",
        ["workspace_id"],
        unique=False
    )

    op.create_table(
        "channels",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "workspace_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True
        ),
        sa.Column(
            "channel_type",
            sa.String(length=50),
            nullable=False,
            server_default="PUBLIC"
        ),
        sa.Column(
            "created_by",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "is_archived",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
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
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["organizations.id"]
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workspace_id",
            "name",
            name="uq_channels_workspace_name"
        )
    )

    op.create_index(
        op.f("ix_channels_channel_type"),
        "channels",
        ["channel_type"],
        unique=False
    )

    op.create_index(
        op.f("ix_channels_created_by"),
        "channels",
        ["created_by"],
        unique=False
    )

    op.create_index(
        op.f("ix_channels_id"),
        "channels",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_channels_is_archived"),
        "channels",
        ["is_archived"],
        unique=False
    )

    op.create_index(
        op.f("ix_channels_tenant_id"),
        "channels",
        ["tenant_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_channels_workspace_id"),
        "channels",
        ["workspace_id"],
        unique=False
    )

    op.create_table(
        "channel_members",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "channel_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        ),
        sa.Column(
            "is_muted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        ),
        sa.Column(
            "last_read_message_id",
            sa.Integer(),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["channel_id"],
            ["channels.id"]
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "channel_id",
            "user_id",
            name="uq_channel_members_channel_user"
        )
    )

    op.create_index(
        op.f("ix_channel_members_channel_id"),
        "channel_members",
        ["channel_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_channel_members_id"),
        "channel_members",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_channel_members_user_id"),
        "channel_members",
        ["user_id"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f("ix_channel_members_user_id"),
        table_name="channel_members"
    )

    op.drop_index(
        op.f("ix_channel_members_id"),
        table_name="channel_members"
    )

    op.drop_index(
        op.f("ix_channel_members_channel_id"),
        table_name="channel_members"
    )

    op.drop_table("channel_members")

    op.drop_index(
        op.f("ix_channels_workspace_id"),
        table_name="channels"
    )

    op.drop_index(
        op.f("ix_channels_tenant_id"),
        table_name="channels"
    )

    op.drop_index(
        op.f("ix_channels_is_archived"),
        table_name="channels"
    )

    op.drop_index(
        op.f("ix_channels_id"),
        table_name="channels"
    )

    op.drop_index(
        op.f("ix_channels_created_by"),
        table_name="channels"
    )

    op.drop_index(
        op.f("ix_channels_channel_type"),
        table_name="channels"
    )

    op.drop_table("channels")

    op.drop_index(
        op.f("ix_workspace_members_workspace_id"),
        table_name="workspace_members"
    )

    op.drop_index(
        op.f("ix_workspace_members_user_id"),
        table_name="workspace_members"
    )

    op.drop_index(
        op.f("ix_workspace_members_role"),
        table_name="workspace_members"
    )

    op.drop_index(
        op.f("ix_workspace_members_is_active"),
        table_name="workspace_members"
    )

    op.drop_index(
        op.f("ix_workspace_members_id"),
        table_name="workspace_members"
    )

    op.drop_table("workspace_members")

    op.drop_index(
        op.f("ix_workspaces_visibility"),
        table_name="workspaces"
    )

    op.drop_index(
        op.f("ix_workspaces_tenant_id"),
        table_name="workspaces"
    )

    op.drop_index(
        op.f("ix_workspaces_slug"),
        table_name="workspaces"
    )

    op.drop_index(
        op.f("ix_workspaces_is_archived"),
        table_name="workspaces"
    )

    op.drop_index(
        op.f("ix_workspaces_id"),
        table_name="workspaces"
    )

    op.drop_index(
        op.f("ix_workspaces_created_by"),
        table_name="workspaces"
    )

    op.drop_table("workspaces")

    op.drop_index(
        op.f("ix_tenant_collaboration_usage_tenant_id"),
        table_name="tenant_collaboration_usage"
    )

    op.drop_index(
        op.f("ix_tenant_collaboration_usage_id"),
        table_name="tenant_collaboration_usage"
    )

    op.drop_table("tenant_collaboration_usage")

    op.drop_index(
        op.f("ix_tenant_collaboration_settings_tenant_id"),
        table_name="tenant_collaboration_settings"
    )

    op.drop_index(
        op.f("ix_tenant_collaboration_settings_id"),
        table_name="tenant_collaboration_settings"
    )

    op.drop_table("tenant_collaboration_settings")

    op.drop_index(
        op.f("ix_tenant_onboarding_tenant_id"),
        table_name="tenant_onboarding"
    )

    op.drop_index(
        op.f("ix_tenant_onboarding_onboarding_status"),
        table_name="tenant_onboarding"
    )

    op.drop_index(
        op.f("ix_tenant_onboarding_id"),
        table_name="tenant_onboarding"
    )

    op.drop_index(
        op.f("ix_tenant_onboarding_admin_user_id"),
        table_name="tenant_onboarding"
    )

    op.drop_table("tenant_onboarding")

    op.drop_index(
        op.f("ix_organizations_status"),
        table_name="organizations"
    )

    op.drop_index(
        op.f("ix_organizations_contact_email"),
        table_name="organizations"
    )

    op.drop_column(
        "organizations",
        "updated_at"
    )

    op.drop_column(
        "organizations",
        "status"
    )

    op.drop_column(
        "organizations",
        "industry"
    )

    op.drop_column(
        "organizations",
        "address"
    )

    op.drop_column(
        "organizations",
        "phone"
    )

    op.drop_column(
        "organizations",
        "contact_email"
    )
