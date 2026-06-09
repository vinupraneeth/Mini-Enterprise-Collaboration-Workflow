from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from datetime import datetime

from typing import Literal

from app.utils.sanitization import (
    require_clean_text,
    sanitize_text
)


class ApprovalCreate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        max_length=2000
    )

    task_id: int | None = None


    @field_validator(
        "title"
    )
    @classmethod
    def clean_title(cls, value):

        return require_clean_text(
            value,
            "Title"
        )


    @field_validator(
        "description"
    )
    @classmethod
    def clean_description(cls, value):

        return sanitize_text(
            value
        )


class ApprovalReview(BaseModel):

    action: Literal["approve", "reject", "hold"]

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


class ApprovalResponse(BaseModel):

    id: int

    title: str

    description: str | None = None

    task_id: int | None = None

    requested_by: int

    reviewed_by: int | None = None

    status: str

    current_level: str | None = None

    remarks: str | None = None

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


class ApprovalHistoryResponse(BaseModel):

    id: int

    approval_id: int

    action_by: int | None = None

    action: str | None = None

    comment: str | None = None

    created_at: datetime


    class Config:

        from_attributes = True
