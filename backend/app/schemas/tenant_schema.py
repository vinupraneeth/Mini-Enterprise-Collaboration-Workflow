from datetime import datetime

from typing import Literal

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)

from app.utils.sanitization import (
    require_clean_text,
    sanitize_text
)


class TenantBase(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150
    )

    contact_email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=30
    )

    address: str | None = Field(
        default=None,
        max_length=2000
    )

    industry: str | None = Field(
        default=None,
        max_length=100
    )


    @field_validator(
        "name"
    )
    @classmethod
    def clean_name(cls, value):

        return require_clean_text(
            value,
            "Tenant name"
        )


    @field_validator(
        "phone",
        "address",
        "industry"
    )
    @classmethod
    def clean_optional_text(cls, value):

        return sanitize_text(
            value
        )


class TenantCreate(TenantBase):

    slug: str | None = Field(
        default=None,
        max_length=120
    )


    @field_validator(
        "slug"
    )
    @classmethod
    def clean_slug(cls, value):

        return sanitize_text(
            value
        )


class TenantUpdate(TenantBase):

    status: Literal[
        "ACTIVE",
        "SUSPENDED",
        "TRIAL",
        "CANCELLED"
    ] = "ACTIVE"


    @field_validator(
        "status",
        mode="before"
    )
    @classmethod
    def clean_status(cls, value):

        return require_clean_text(
            value,
            "Tenant status"
        ).upper()


class TenantResponse(BaseModel):

    id: int

    name: str

    slug: str

    contact_email: EmailStr | None = None

    phone: str | None = None

    address: str | None = None

    industry: str | None = None

    status: str

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:

        from_attributes = True


class TenantAdminCreate(BaseModel):

    admin_name: str = Field(
        min_length=1,
        max_length=100
    )

    admin_email: EmailStr

    admin_password: str = Field(
        min_length=6,
        max_length=128
    )

    create_default_workspace: bool = True


    @field_validator(
        "admin_name"
    )
    @classmethod
    def clean_admin_name(cls, value):

        return require_clean_text(
            value,
            "Admin name"
        )


class TenantOnboardRequest(TenantCreate, TenantAdminCreate):

    pass


class TenantOnboardingResponse(BaseModel):

    id: int

    tenant_id: int

    admin_user_id: int | None = None

    onboarding_status: str

    default_workspace_created: bool

    settings_created: bool

    completed_at: datetime | None = None

    created_at: datetime | None = None

    class Config:

        from_attributes = True


class TenantOnboardResponse(BaseModel):

    tenant: TenantResponse

    onboarding: TenantOnboardingResponse


class TenantCollaborationSettingsUpdate(BaseModel):

    max_workspaces: int = Field(
        gt=0
    )

    max_channels_per_workspace: int = Field(
        gt=0
    )

    max_workspace_members: int = Field(
        gt=0
    )

    max_storage_mb: int = Field(
        gt=0
    )

    workspace_enabled: bool = True

    channel_enabled: bool = True


class TenantCollaborationSettingsResponse(BaseModel):

    id: int

    tenant_id: int

    max_workspaces: int

    max_channels_per_workspace: int

    max_workspace_members: int

    max_storage_mb: int

    workspace_enabled: bool

    channel_enabled: bool

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:

        from_attributes = True


class TenantCollaborationUsageResponse(BaseModel):

    id: int

    tenant_id: int

    workspace_count: int

    channel_count: int

    member_count: int

    storage_used_mb: int

    last_calculated_at: datetime | None = None

    class Config:

        from_attributes = True
