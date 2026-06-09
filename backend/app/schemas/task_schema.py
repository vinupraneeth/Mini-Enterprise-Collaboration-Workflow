from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from datetime import datetime

from app.utils.sanitization import (
    require_clean_text,
    sanitize_text
)


class TaskCreate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str = Field(
        min_length=1,
        max_length=2000
    )

    priority: Literal[
        "low",
        "medium",
        "high"
    ] = "medium"

    due_date: datetime | None = None

    assigned_to: int = Field(
        gt=0
    )


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

        return require_clean_text(
            value,
            "Description"
        )


class TaskUpdate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str = Field(
        min_length=1,
        max_length=2000
    )

    priority: Literal[
        "low",
        "medium",
        "high"
    ]

    due_date: datetime | None = None

    assigned_to: int = Field(
        gt=0
    )


    @field_validator(
        "title"
    )
    @classmethod
    def clean_update_title(cls, value):

        return require_clean_text(
            value,
            "Title"
        )


    @field_validator(
        "description"
    )
    @classmethod
    def clean_update_description(cls, value):

        return require_clean_text(
            value,
            "Description"
        )


class TaskStatusUpdate(BaseModel):

    status: Literal[
        "todo",
        "in_progress",
        "review",
        "done"
    ]

class TaskAssign(BaseModel):

    assigned_to: int = Field(
        gt=0
    )

class TaskResponse(BaseModel):

    id: int

    title: str

    description: str

    status: str

    priority: str

    due_date: datetime | None = None

    assigned_to: int

    assigned_to_name: str | None = None

    created_by: int

    created_by_name: str | None = None

    created_at: datetime | None = None

    approval_status: str | None = None

    approval_remarks: str | None = None

    class Config:

        from_attributes = True


class TaskHistoryResponse(BaseModel):

    id: int
    task_id: int
    old_status: str
    new_status: str
    changed_by: int
    created_at: datetime

    class Config:
        from_attributes = True
