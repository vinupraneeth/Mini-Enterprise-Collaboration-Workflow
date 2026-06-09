from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.user_model import User

from app.schemas.user_schema import (
    UserResponse
)

from app.core.dependencies import (
    get_current_user,
    require_admin
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=Page[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(
        require_admin
    )
):

    return paginate(
        db,
        select(User).where(
            User.organization_id ==
            current_user.organization_id
        )
    )


@router.get(
    "/employees",
    response_model=Page[UserResponse]
)
def get_employees(
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    if current_user.role.lower() not in [
        "admin",
        "manager"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return paginate(
        db,
        select(User).where(
            User.role == "employee",
            User.organization_id ==
            current_user.organization_id
        )
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    result = db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if (
        current_user.role.lower() != "admin"
        and
        current_user.id != user_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Users can view only their own profile"
        )

    if (
        current_user.role.lower() == "admin"
        and
        user.organization_id != current_user.organization_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Users can view only their own organization"
        )

    return user
