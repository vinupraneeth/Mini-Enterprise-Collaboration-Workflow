from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime,
    Boolean
)

from sqlalchemy.sql import func

from app.db.database import Base


class TaskComment(Base):

    __tablename__ = "task_comments"

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

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    comment = Column(
        Text,
        nullable=False
    )

    is_internal = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )