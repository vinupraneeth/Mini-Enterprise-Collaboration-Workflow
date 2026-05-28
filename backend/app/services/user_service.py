from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user_schema import (
    UserCreate,
    LoginRequest
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
    create_access_token
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

    return {

        "access_token": access_token,

        "token_type": "bearer",

        "name": user.name,

        "role": user.role
    }
