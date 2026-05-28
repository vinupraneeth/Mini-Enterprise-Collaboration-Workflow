from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.services.activity_service import (
    fetch_activity_feed
)

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(

    prefix="/activity",

    tags=["Activity Feed"]
)


@router.get("/")
def get_activity_feed_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return fetch_activity_feed(db)