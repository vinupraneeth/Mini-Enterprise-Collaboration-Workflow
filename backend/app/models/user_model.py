from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
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

    assigned_tasks = relationship(
        "Task",
        foreign_keys="Task.assigned_to",
        overlaps="assignee"
    )

    created_tasks = relationship(
        "Task",
        foreign_keys="Task.created_by",
        overlaps="creator"
    )

    updated_tasks = relationship(
        "Task",
        foreign_keys="Task.updated_by",
        overlaps="updater"
    )
