from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def handle_db_commit(db):

    try:

        db.commit()

    except IntegrityError as error:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint error. Duplicate or invalid related record."
        ) from error

    except SQLAlchemyError as error:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed."
        ) from error
