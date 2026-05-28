from pydantic import BaseModel

from datetime import datetime


class TaskCommentCreate(BaseModel):

    comment: str

    is_internal: bool = False


class TaskCommentResponse(BaseModel):

    id: int

    task_id: int

    user_id: int

    user_name: str

    comment: str

    is_internal: bool

    created_at: datetime

    class Config:

        from_attributes = True