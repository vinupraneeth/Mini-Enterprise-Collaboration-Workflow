from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.security import (
    oauth2_scheme,
    verify_access_token
)
from app.repositories.user_repository import (
    get_user_by_email
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_access_token(token)

    email = payload.get("email")

    user = get_user_by_email(
        db,
        email
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def require_admin(
    current_user = Depends(get_current_user)
):

    return require_roles(
        [
            "admin"
        ]
    )(
        current_user
    )


def require_roles(
    allowed_roles: list[str]
):

    normalized_roles = [
        role.lower()
        for role in allowed_roles
    ]

    def role_checker(
        current_user = Depends(get_current_user)
    ):

        if current_user.role.lower() not in normalized_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_user

    return role_checker


def require_manager_or_admin(
    current_user = Depends(get_current_user)
):

    return require_roles(
        [
            "admin",
            "manager"
        ]
    )(
        current_user
    )
