from pydantic import BaseModel

from datetime import datetime

from typing import Literal


class ApprovalCreate(BaseModel):

    title: str

    description: str | None = None

    task_id: int | None = None


class ApprovalReview(BaseModel):

    action: Literal["approve", "reject", "hold"]

    comment: str | None = None


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