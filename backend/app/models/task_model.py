from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
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


class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="todo"
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        default="medium"
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    assigned_to: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id")
    )

    updated_by: Mapped[int | None] = mapped_column(
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

    assignee = relationship(
        "User",
        foreign_keys=[assigned_to],
        overlaps="assigned_tasks"
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
        overlaps="created_tasks"
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by],
        overlaps="updated_tasks"
    )
