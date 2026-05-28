from sqlalchemy import (
    Column,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from app.db.database import Base

from sqlalchemy import Boolean, DateTime

from sqlalchemy.sql import func


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False
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

    is_active = Column(
        Boolean,
        default=True
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