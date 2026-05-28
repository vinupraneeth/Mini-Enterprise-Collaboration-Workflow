from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.db.database import Base


class Task(Base):

    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        default="todo"
    )

    priority = Column(
        String(50),
        default="medium"
    )

    due_date = Column(
        DateTime,
        nullable=True
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    updated_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
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