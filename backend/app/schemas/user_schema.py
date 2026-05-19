from pydantic import BaseModel, EmailStr
from datetime import datetime

#REGISTRATION SCHEMA

class UserBase(BaseModel):

    name: str

    email: EmailStr

    role: str


class UserCreate(UserBase):

    password: str


class UserResponse(UserBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True


#LOGIN SCHEMAS

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str