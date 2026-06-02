from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    require_admin
)

from app.db.deps import get_db

from app.schemas.audit_log_schema import (
    AuditLogResponse
)

from app.services.audit_log_service import (
    get_audit_logs_statement
)


router = APIRouter(

    prefix="/audit-logs",

    tags=["Audit Logs"]
)


@router.get(
    "/",
    response_model=Page[AuditLogResponse]
)
def get_audit_logs_api(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return paginate(
        db,
        get_audit_logs_statement()
    )
