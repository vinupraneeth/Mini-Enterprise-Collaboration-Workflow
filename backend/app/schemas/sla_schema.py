from datetime import datetime

from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from app.utils.sanitization import (
    require_clean_text
)


class SLARuleCreate(BaseModel):

    module_name: Literal[
        "task",
        "approval"
    ]

    priority: Literal[
        "low",
        "medium",
        "high"
    ]

    allowed_hours: int = Field(
        gt=0
    )

    escalation_enabled: bool = False

    escalation_after_hours: int | None = Field(
        default=None,
        gt=0
    )

    is_active: bool = True


    @field_validator(
        "module_name",
        "priority",
        mode="before"
    )
    @classmethod
    def clean_text_fields(cls, value):

        return require_clean_text(
            value,
            "SLA field"
        ).lower()


class SLARuleUpdate(BaseModel):

    module_name: Literal[
        "task",
        "approval"
    ]

    priority: Literal[
        "low",
        "medium",
        "high"
    ]

    allowed_hours: int = Field(
        gt=0
    )

    escalation_enabled: bool = False

    escalation_after_hours: int | None = Field(
        default=None,
        gt=0
    )

    is_active: bool = True


    @field_validator(
        "module_name",
        "priority",
        mode="before"
    )
    @classmethod
    def clean_update_text_fields(cls, value):

        return require_clean_text(
            value,
            "SLA field"
        ).lower()


class SLARuleResponse(BaseModel):

    id: int

    module_name: str

    priority: str

    allowed_hours: int

    escalation_enabled: bool

    escalation_after_hours: int | None = None

    is_active: bool

    created_by: int | None = None

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:

        from_attributes = True


class SLATrackingResponse(BaseModel):

    id: int

    module_name: str

    record_id: int

    sla_rule_id: int

    start_time: datetime

    due_time: datetime

    completed_time: datetime | None = None

    status: str

    breach_reason: str | None = None

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:

        from_attributes = True
