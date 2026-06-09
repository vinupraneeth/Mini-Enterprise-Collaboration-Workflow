from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from datetime import datetime

from app.utils.sanitization import (
    require_clean_text
)


class TaskCommentCreate(BaseModel):

    comment: str = Field(
        min_length=1,
        max_length=2000
    )

    is_internal: bool = False


    @field_validator(
        "comment"
    )
    @classmethod
    def clean_comment(cls, value):

        return require_clean_text(
            value,
            "Comment"
        )


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
