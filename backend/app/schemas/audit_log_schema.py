from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):

    id: int

    user_id: int | None = None

    action: str

    entity: str

    entity_id: int | None = None

    module_name: str | None = None

    action_type: str | None = None

    record_id: int | None = None

    old_data: str | None = None

    new_data: str | None = None

    ip_address: str | None = None

    user_agent: str | None = None

    timestamp: datetime | None = None

    class Config:

        from_attributes = True
