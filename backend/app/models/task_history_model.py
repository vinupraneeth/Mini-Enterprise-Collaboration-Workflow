from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.db.database import Base


class TaskHistory(Base):

    __tablename__ = "task_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=False
    )

    old_status = Column(
        String(50),
        nullable=False
    )

    new_status = Column(
        String(50),
        nullable=False
    )

    changed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )