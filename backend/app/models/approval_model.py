from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text
)

from sqlalchemy.sql import func

from app.db.database import Base

from sqlalchemy.orm import relationship

class Approval(Base):

    __tablename__ = "approvals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False,
        default="Task approval request"
    )

    description = Column(
        Text,
        nullable=True
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=True
    )

    requested_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    reviewed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    status = Column(
        String(50),
        default="pending"
    )

    current_level = Column(
        String(50),
        default="manager"
    )

    remarks = Column(
        Text,
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

    task = relationship(
        "Task"
    )
