from datetime import datetime

from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from app.utils.sanitization import (
    require_clean_text,
    sanitize_text
)


class ChannelCreate(BaseModel):

    workspace_id: int = Field(
        gt=0
    )

    name: str = Field(
        min_length=1,
        max_length=150
    )

    description: str | None = Field(
        default=None,
        max_length=2000
    )

    channel_type: Literal[
        "PUBLIC",
        "PRIVATE",
        "ANNOUNCEMENT",
        "PROJECT"
    ] = "PUBLIC"


    @field_validator(
        "name"
    )
    @classmethod
    def clean_name(cls, value):

        return require_clean_text(
            value,
            "Channel name"
        )


    @field_validator(
        "description"
    )
    @classmethod
    def clean_description(cls, value):

        return sanitize_text(
            value
        )


    @field_validator(
        "channel_type",
        mode="before"
    )
    @classmethod
    def clean_channel_type(cls, value):

        return require_clean_text(
            value,
            "Channel type"
        ).upper()


class ChannelUpdate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150
    )

    description: str | None = Field(
        default=None,
        max_length=2000
    )

    channel_type: Literal[
        "PUBLIC",
        "PRIVATE",
        "ANNOUNCEMENT",
        "PROJECT"
    ] = "PUBLIC"


    @field_validator(
        "name"
    )
    @classmethod
    def clean_update_name(cls, value):

        return require_clean_text(
            value,
            "Channel name"
        )


    @field_validator(
        "description"
    )
    @classmethod
    def clean_update_description(cls, value):

        return sanitize_text(
            value
        )


    @field_validator(
        "channel_type",
        mode="before"
    )
    @classmethod
    def clean_update_channel_type(cls, value):

        return require_clean_text(
            value,
            "Channel type"
        ).upper()


class ChannelResponse(BaseModel):

    id: int

    tenant_id: int

    workspace_id: int

    name: str

    description: str | None = None

    channel_type: str

    created_by: int

    is_archived: bool

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:

        from_attributes = True


class ChannelMemberResponse(BaseModel):

    id: int

    channel_id: int

    user_id: int

    joined_at: datetime | None = None

    is_muted: bool

    last_read_message_id: int | None = None

    class Config:

        from_attributes = True
