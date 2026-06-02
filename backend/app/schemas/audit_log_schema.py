from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):

    id: int

    user_id: int | None = None

    action: str

    entity: str

    entity_id: int | None = None

    timestamp: datetime | None = None

    class Config:

        from_attributes = True
