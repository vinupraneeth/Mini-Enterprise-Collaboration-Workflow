from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy.sql import func

from app.db.database import Base


class ApprovalHistory(Base):

    __tablename__ = "approval_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    approval_id: Mapped[int] = mapped_column(
        ForeignKey("approvals.id"),
        nullable=False
    )

    action_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    action: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    old_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    new_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    changed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
