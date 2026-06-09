from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)

from datetime import datetime

from app.utils.sanitization import (
    require_clean_text
)


class UserCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )

    role: str


    @field_validator(
        "name"
    )
    @classmethod
    def clean_name(cls, value):

        return require_clean_text(
            value,
            "Name"
        )


    @field_validator(
        "role"
    )
    @classmethod
    def clean_role(cls, value):

        return require_clean_text(
            value,
            "Role"
        ).lower()


class LoginRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128
    )


class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: str

    organization_id: int | None = None

    is_active: bool = True

    created_at: datetime | None = None
    
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str

    id: int

    role: str

    name: str

class UserLogin(BaseModel):

    email: EmailStr

    password: str


class RefreshTokenRequest(BaseModel):

    refresh_token: str


class PasswordResetRequest(BaseModel):

    email: EmailStr


class PasswordResetRequestResponse(BaseModel):

    message: str

    reset_token: str | None = None


class PasswordResetConfirm(BaseModel):

    token: str

    new_password: str = Field(
        min_length=6,
        max_length=128
    )


class PasswordResetConfirmResponse(BaseModel):

    message: str
