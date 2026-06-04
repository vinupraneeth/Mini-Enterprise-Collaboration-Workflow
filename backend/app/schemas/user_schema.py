from pydantic import (
    BaseModel,
    EmailStr
)

from datetime import datetime


class UserCreate(BaseModel):

    name: str

    email: EmailStr

    password: str

    role: str


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: str

    is_active: bool = True

    created_at: datetime | None = None
    
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):

    access_token: str

    token_type: str

    id: int

    role: str

    name: str

class UserLogin(BaseModel):

    email: EmailStr

    password: str
