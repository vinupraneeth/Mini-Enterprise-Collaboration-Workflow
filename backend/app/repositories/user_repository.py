from app.utils.db_exceptions import (
    handle_db_commit
)

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.models.user_model import User


def get_user_by_email( db: Session, email: str ):
    
    result = db.execute(
        select(User).where(
            User.email == email
        )
    )

    return result.scalar_one_or_none()


def create_user( db: Session, user_data: dict ):

    user = User(**user_data)
    db.add(user)
    handle_db_commit(db)
    db.refresh(user)

    return user
