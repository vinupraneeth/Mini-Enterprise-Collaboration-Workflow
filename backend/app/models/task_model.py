from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from datetime import datetime, UTC

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
        ForeignKey("users.id")
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default=lambda:
            datetime.now(UTC)
    )

    updated_at = Column(
        DateTime,
        default=lambda:
            datetime.now(UTC),

        onupdate=lambda:
            datetime.now(UTC)
    )


    assigned_user = relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_tasks"
    )

    creator_user = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_tasks"
    )