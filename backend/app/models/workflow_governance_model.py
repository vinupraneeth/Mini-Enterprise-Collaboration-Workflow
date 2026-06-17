from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.db.database import Base


class SLARule(Base):

    __tablename__ = "sla_rules"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    module_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    allowed_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    escalation_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    escalation_after_hours: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        index=True
    )

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
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

    creator = relationship(
        "User",
        foreign_keys=[created_by]
    )


class SLATracking(Base):

    __tablename__ = "sla_tracking"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    module_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    record_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    sla_rule_id: Mapped[int] = mapped_column(
        ForeignKey("sla_rules.id"),
        nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    due_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    completed_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    breach_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
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

    sla_rule = relationship(
        "SLARule"
    )


class ApprovalEscalation(Base):

    __tablename__ = "approval_escalations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    approval_id: Mapped[int] = mapped_column(
        ForeignKey("approvals.id"),
        nullable=False,
        index=True
    )

    escalated_from: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    escalated_to: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    escalation_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        index=True
    )

    escalated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    approval = relationship(
        "Approval"
    )

    from_user = relationship(
        "User",
        foreign_keys=[escalated_from]
    )

    to_user = relationship(
        "User",
        foreign_keys=[escalated_to]
    )


class ApprovalDelegation(Base):

    __tablename__ = "approval_delegations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    delegator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    delegatee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        index=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    delegator = relationship(
        "User",
        foreign_keys=[delegator_id]
    )

    delegatee = relationship(
        "User",
        foreign_keys=[delegatee_id]
    )


class NotificationPreference(Base):

    __tablename__ = "notification_preferences"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    in_app_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    email_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    task_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    approval_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    escalation_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    document_notifications: Mapped[bool] = mapped_column(
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

    user = relationship(
        "User"
    )
