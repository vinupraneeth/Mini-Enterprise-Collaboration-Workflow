from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy.sql import func

from app.db.database import Base


class TaskHistory(Base):

    __tablename__ = "task_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    old_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    new_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    changed_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
