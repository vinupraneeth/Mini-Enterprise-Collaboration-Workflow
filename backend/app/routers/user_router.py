from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

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
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(
        require_admin
    )
):

    users = db.query(User).all()

    return users


@router.get(
    "/employees",
    response_model=list[UserResponse]
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

    return db.query(User).filter(
        User.role == "employee"
    ).all()


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

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
