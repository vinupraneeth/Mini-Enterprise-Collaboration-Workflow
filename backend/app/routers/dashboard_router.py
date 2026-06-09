from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.services.dashboard_service import (
    get_dashboard_analytics,
    get_ai_summary,
    get_role_dashboard,
    get_smart_assignment
)

from app.core.dependencies import (
    get_current_user
)

from app.schemas.dashboard_schema import (
    AiSummaryResponse,
    SmartAssignmentResponse
)


router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"]
)


@router.get("/analytics")
def dashboard_analytics_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return get_dashboard_analytics( db, current_user )


@router.get("/summary")
def dashboard_summary_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return get_dashboard_analytics(
        db,
        current_user
    )


@router.get("/task-distribution")
def dashboard_task_distribution_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    analytics = get_dashboard_analytics(
        db,
        current_user
    )

    return analytics["tasks"]


@router.get(
    "/ai-summary",
    response_model=AiSummaryResponse
)
def dashboard_ai_summary_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return get_ai_summary(
        db,
        current_user
    )


@router.get(
    "/role-view"
)
def dashboard_role_view_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return get_role_dashboard(
        db,
        current_user
    )


@router.get(
    "/smart-assignment",
    response_model=SmartAssignmentResponse
)
def dashboard_smart_assignment_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return get_smart_assignment(
        db,
        current_user
    )
