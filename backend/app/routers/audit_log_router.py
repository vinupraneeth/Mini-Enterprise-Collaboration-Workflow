from fastapi import (
    APIRouter,
    Depends,
    Query
)

from datetime import datetime

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    require_admin_or_auditor
)

from app.db.deps import get_db

from app.schemas.audit_log_schema import (
    AuditLogResponse
)

from app.services.audit_log_service import (
    get_audit_log_by_id,
    get_audit_logs_by_date_range_statement,
    get_audit_logs_by_module_statement,
    get_audit_logs_by_user_statement,
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
        require_admin_or_auditor
    )
):

    return paginate(
        db,
        get_audit_logs_statement()
    )


@router.get(
    "/date-range",
    response_model=Page[AuditLogResponse]
)
def get_audit_logs_by_date_range_api(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(
        require_admin_or_auditor
    )
):

    return paginate(
        db,
        get_audit_logs_by_date_range_statement(
            start_date,
            end_date
        )
    )


@router.get(
    "/module/{module_name}",
    response_model=Page[AuditLogResponse]
)
def get_audit_logs_by_module_api(
    module_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_admin_or_auditor
    )
):

    return paginate(
        db,
        get_audit_logs_by_module_statement(
            module_name
        )
    )


@router.get(
    "/user/{user_id}",
    response_model=Page[AuditLogResponse]
)
def get_audit_logs_by_user_api(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_admin_or_auditor
    )
):

    return paginate(
        db,
        get_audit_logs_by_user_statement(
            user_id
        )
    )


@router.get(
    "/{log_id}",
    response_model=AuditLogResponse
)
def get_audit_log_api(
    log_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_admin_or_auditor
    )
):

    return get_audit_log_by_id(
        db,
        log_id
    )
