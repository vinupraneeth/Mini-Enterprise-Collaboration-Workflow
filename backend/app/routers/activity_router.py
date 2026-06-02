from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page, Params, paginate

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


@router.get(
    "/",
    response_model=Page[dict]
)
def get_activity_feed_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    ),

    params: Params = Depends()
):

    return paginate(
        fetch_activity_feed(
            db,
            current_user
        ),
        params
    )
