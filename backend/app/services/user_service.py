from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user_schema import (
    UserCreate,
    LoginRequest,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm
)

from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)

from app.utils.hashing import (
    hash_password,
    verify_password
)

from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    hash_token,
    verify_refresh_token
)

from app.core.config import (
    REFRESH_TOKEN_EXPIRE_DAYS,
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
)

from app.models.auth_token_model import (
    RefreshToken,
    PasswordResetToken
)

from app.models.user_model import (
    User
)

from app.services.saas_service import (
    get_default_organization
)


def register_user(
    db: Session,
    user: UserCreate
):

    valid_roles = [
        "admin",
        "manager",
        "employee"
    ]

    user_role = user.role.lower()

    if user_role not in valid_roles:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user role"
        )

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pw = hash_password(user.password)

    user_data = user.model_dump()

    user_data.pop("password")

    user_data["hashed_password"] = hashed_pw

    user_data["role"] = user_role

    organization = get_default_organization(
        db
    )

    user_data["organization_id"] = organization.id

    return create_user(
        db,
        user_data
    )


def login_user(
    db: Session,
    login_data: LoginRequest
):

    user = get_user_by_email(
        db,
        login_data.email
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    is_password_valid = verify_password(
        login_data.password,
        user.hashed_password
    )

    if not is_password_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": user.email
        }
    )

    refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    )

    db.add(refresh_token_record)

    db.commit()

    return {

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "id": user.id,

        "name": user.name,

        "role": user.role
    }


def refresh_access_token(
    db: Session,
    token_data: RefreshTokenRequest
):

    payload = verify_refresh_token(
        token_data.refresh_token
    )

    token_hash = hash_token(
        token_data.refresh_token
    )

    refresh_token_record = db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked.is_(False)
        )
    ).scalar_one_or_none()

    if not refresh_token_record:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found or revoked"
        )

    expires_at = refresh_token_record.expires_at

    if expires_at.tzinfo is None:

        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at < datetime.now(timezone.utc):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )

    user = get_user_by_email(
        db,
        payload.get("email")
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    return {

        "access_token": access_token,

        "refresh_token": token_data.refresh_token,

        "token_type": "bearer",

        "id": user.id,

        "name": user.name,

        "role": user.role
    }


def request_password_reset(
    db: Session,
    reset_data: PasswordResetRequest
):

    user = get_user_by_email(
        db,
        reset_data.email
    )

    if not user:

        return {

            "message": "If the email exists, a password reset token has been generated.",

            "reset_token": None
        }

    reset_token = create_password_reset_token(
        data={
            "sub": user.email
        }
    )

    reset_token_record = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_token(reset_token),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
        used=False
    )

    db.add(reset_token_record)

    db.commit()

    return {

        "message": "Password reset token generated. In production this token would be sent by email.",

        "reset_token": reset_token
    }


def confirm_password_reset(
    db: Session,
    reset_data: PasswordResetConfirm
):

    token_hash = hash_token(
        reset_data.token
    )

    reset_token_record = db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used.is_(False)
        )
    ).scalar_one_or_none()

    if not reset_token_record:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already used reset token"
        )

    expires_at = reset_token_record.expires_at

    if expires_at.tzinfo is None:

        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at < datetime.now(timezone.utc):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token expired"
        )

    user = db.execute(
        select(User).where(
            User.id == reset_token_record.user_id
        )
    ).scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.hashed_password = hash_password(
        reset_data.new_password
    )

    reset_token_record.used = True

    db.commit()

    return {

        "message": "Password reset successful. You can now login with the new password."
    }
