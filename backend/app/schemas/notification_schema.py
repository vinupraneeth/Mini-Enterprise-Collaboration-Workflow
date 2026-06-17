from datetime import datetime

from pydantic import BaseModel


class NotificationResponse(BaseModel):

    id: int

    user_id: int

    message: str

    notification_type: str | None = None

    priority: str | None = None

    is_read: bool

    created_at: datetime | None = None

    class Config:

        from_attributes = True
