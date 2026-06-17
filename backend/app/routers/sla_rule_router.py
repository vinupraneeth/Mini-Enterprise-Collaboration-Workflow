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

from app.schemas.sla_schema import (
    SLARuleCreate,
    SLARuleResponse,
    SLARuleUpdate
)

from app.services.sla_service import (
    create_sla_rule,
    disable_sla_rule,
    get_sla_rule_by_id,
    get_sla_rules_statement,
    update_sla_rule
)


router = APIRouter(

    prefix="/sla-rules",

    tags=["SLA Rules"]
)


@router.post(
    "/",
    response_model=SLARuleResponse,
    status_code=201
)
def create_sla_rule_api(
    rule_data: SLARuleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_sla_rule(
        db,
        rule_data,
        current_user
    )


@router.get(
    "/",
    response_model=Page[SLARuleResponse]
)
def get_sla_rules_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return paginate(
        db,
        get_sla_rules_statement()
    )


@router.get(
    "/{rule_id}",
    response_model=SLARuleResponse
)
def get_sla_rule_api(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return get_sla_rule_by_id(
        db,
        rule_id
    )


@router.put(
    "/{rule_id}",
    response_model=SLARuleResponse
)
def update_sla_rule_api(
    rule_id: int,
    rule_data: SLARuleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return update_sla_rule(
        db,
        rule_id,
        rule_data,
        current_user
    )


@router.delete(
    "/{rule_id}",
    response_model=SLARuleResponse
)
def disable_sla_rule_api(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return disable_sla_rule(
        db,
        rule_id,
        current_user
    )
