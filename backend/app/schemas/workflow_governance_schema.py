from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator
)

from app.utils.sanitization import (
    require_clean_text,
    sanitize_text
)


class ApprovalEscalationCreate(BaseModel):

    approval_id: int = Field(
        gt=0
    )

    escalated_to: int = Field(
        gt=0
    )

    reason: str = Field(
        min_length=1,
        max_length=2000
    )


    @field_validator(
        "reason"
    )
    @classmethod
    def clean_reason(cls, value):

        return require_clean_text(
            value,
            "Reason"
        )


class ApprovalEscalationResolve(BaseModel):

    comment: str | None = Field(
        default=None,
        max_length=2000
    )


    @field_validator(
        "comment"
    )
    @classmethod
    def clean_comment(cls, value):

        return sanitize_text(
            value
        )


class ApprovalEscalationResponse(BaseModel):

    id: int

    approval_id: int

    escalated_from: int

    escalated_to: int

    reason: str

    escalation_level: int

    status: str

    escalated_at: datetime | None = None

    resolved_at: datetime | None = None

    class Config:

        from_attributes = True


class ApprovalDelegationCreate(BaseModel):

    delegatee_id: int = Field(
        gt=0
    )

    start_date: datetime

    end_date: datetime

    reason: str = Field(
        min_length=1,
        max_length=2000
    )


    @field_validator(
        "reason"
    )
    @classmethod
    def clean_delegation_reason(cls, value):

        return require_clean_text(
            value,
            "Reason"
        )


    @model_validator(
        mode="after"
    )
    def validate_date_range(self):

        if self.end_date <= self.start_date:

            raise ValueError(
                "End date must be after start date"
            )

        return self


class ApprovalDelegationResponse(BaseModel):

    id: int

    delegator_id: int

    delegatee_id: int

    start_date: datetime

    end_date: datetime

    reason: str

    is_active: bool

    created_at: datetime | None = None

    class Config:

        from_attributes = True


class NotificationPreferenceUpdate(BaseModel):

    in_app_enabled: bool = True

    email_enabled: bool = False

    task_notifications: bool = True

    approval_notifications: bool = True

    escalation_notifications: bool = True

    document_notifications: bool = True


class NotificationPreferenceResponse(BaseModel):

    id: int

    user_id: int

    in_app_enabled: bool

    email_enabled: bool

    task_notifications: bool

    approval_notifications: bool

    escalation_notifications: bool

    document_notifications: bool

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:

        from_attributes = True
