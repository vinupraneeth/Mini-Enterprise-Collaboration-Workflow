from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.db.database import Base


class TenantOnboarding(Base):

    __tablename__ = "tenant_onboarding"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        unique=True,
        index=True
    )

    admin_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    onboarding_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING",
        index=True
    )

    default_workspace_created: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    settings_created: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    tenant = relationship(
        "Organization"
    )

    admin_user = relationship(
        "User"
    )


class TenantCollaborationSettings(Base):

    __tablename__ = "tenant_collaboration_settings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        unique=True,
        index=True
    )

    max_workspaces: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5
    )

    max_channels_per_workspace: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10
    )

    max_workspace_members: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=50
    )

    max_storage_mb: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1024
    )

    workspace_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    channel_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    tenant = relationship(
        "Organization"
    )


class TenantCollaborationUsage(Base):

    __tablename__ = "tenant_collaboration_usage"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        unique=True,
        index=True
    )

    workspace_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    channel_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    member_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    storage_used_mb: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    last_calculated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    tenant = relationship(
        "Organization"
    )


class Workspace(Base):

    __tablename__ = "workspaces"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "slug",
            name="uq_workspaces_tenant_slug"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    visibility: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PUBLIC",
        index=True
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    tenant = relationship(
        "Organization"
    )

    creator = relationship(
        "User"
    )


class WorkspaceMember(Base):

    __tablename__ = "workspace_members"

    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "user_id",
            name="uq_workspace_members_workspace_user"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="MEMBER",
        index=True
    )

    joined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        index=True
    )

    workspace = relationship(
        "Workspace"
    )

    user = relationship(
        "User"
    )


class Channel(Base):

    __tablename__ = "channels"

    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "name",
            name="uq_channels_workspace_name"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    channel_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PUBLIC",
        index=True
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    tenant = relationship(
        "Organization"
    )

    workspace = relationship(
        "Workspace"
    )

    creator = relationship(
        "User"
    )


class ChannelMember(Base):

    __tablename__ = "channel_members"

    __table_args__ = (
        UniqueConstraint(
            "channel_id",
            "user_id",
            name="uq_channel_members_channel_user"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id"),
        nullable=False,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    joined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    is_muted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    last_read_message_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    channel = relationship(
        "Channel"
    )

    user = relationship(
        "User"
    )
