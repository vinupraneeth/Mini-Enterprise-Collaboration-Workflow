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


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    action: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    entity: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    module_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    action_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    record_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    old_data: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    new_data: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
