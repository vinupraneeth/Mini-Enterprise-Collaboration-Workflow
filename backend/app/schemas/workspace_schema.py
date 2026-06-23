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


class WorkspaceCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150
    )

    slug: str | None = Field(
        default=None,
        max_length=150
    )

    description: str | None = Field(
        default=None,
        max_length=2000
    )

    avatar_url: str | None = Field(
        default=None,
        max_length=500
    )

    visibility: Literal[
        "PUBLIC",
        "PRIVATE"
    ] = "PUBLIC"


    @field_validator(
        "name"
    )
    @classmethod
    def clean_name(cls, value):

        return require_clean_text(
            value,
            "Workspace name"
        )


    @field_validator(
        "slug",
        "description",
        "avatar_url"
    )
    @classmethod
    def clean_optional_text(cls, value):

        return sanitize_text(
            value
        )


    @field_validator(
        "visibility",
        mode="before"
    )
    @classmethod
    def clean_visibility(cls, value):

        return require_clean_text(
            value,
            "Visibility"
        ).upper()


class WorkspaceUpdate(WorkspaceCreate):

    pass


class WorkspaceResponse(BaseModel):

    id: int

    tenant_id: int

    name: str

    slug: str

    description: str | None = None

    avatar_url: str | None = None

    visibility: str

    created_by: int

    is_archived: bool

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:

        from_attributes = True


class WorkspaceMemberCreate(BaseModel):

    user_id: int = Field(
        gt=0
    )

    role: Literal[
        "WORKSPACE_ADMIN",
        "MODERATOR",
        "MEMBER",
        "VIEWER"
    ] = "MEMBER"


    @field_validator(
        "role",
        mode="before"
    )
    @classmethod
    def clean_member_role(cls, value):

        return require_clean_text(
            value,
            "Workspace member role"
        ).upper()


class WorkspaceMemberRoleUpdate(BaseModel):

    role: Literal[
        "WORKSPACE_ADMIN",
        "MODERATOR",
        "MEMBER",
        "VIEWER"
    ]


    @field_validator(
        "role",
        mode="before"
    )
    @classmethod
    def clean_update_role(cls, value):

        return require_clean_text(
            value,
            "Workspace member role"
        ).upper()


class WorkspaceMemberResponse(BaseModel):

    id: int

    workspace_id: int

    user_id: int

    role: str

    joined_at: datetime | None = None

    is_active: bool

    class Config:

        from_attributes = True
