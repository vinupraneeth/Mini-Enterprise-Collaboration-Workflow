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

from app.schemas.tenant_schema import (
    TenantCollaborationSettingsResponse,
    TenantCollaborationSettingsUpdate,
    TenantCollaborationUsageResponse,
    TenantAdminCreate,
    TenantCreate,
    TenantOnboardRequest,
    TenantOnboardResponse,
    TenantOnboardingResponse,
    TenantResponse,
    TenantUpdate
)

from app.services.tenant_service import (
    activate_tenant,
    create_tenant,
    create_tenant_admin,
    ensure_platform_admin,
    get_collaboration_settings,
    get_collaboration_usage,
    get_onboarding_status,
    get_tenant_or_404,
    get_tenants_statement,
    onboard_tenant,
    recalculate_collaboration_usage,
    suspend_tenant,
    update_collaboration_settings,
    update_tenant
)


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


@router.post(
    "/",
    response_model=TenantResponse,
    status_code=201
)
def create_tenant_api(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_tenant(
        db,
        tenant_data,
        current_user
    )


@router.get(
    "/",
    response_model=Page[TenantResponse]
)
def get_tenants_api(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return paginate(
        db,
        get_tenants_statement(
            db,
            current_user
        )
    )


@router.post(
    "/onboard",
    response_model=TenantOnboardResponse,
    status_code=201
)
def onboard_tenant_api(
    onboard_data: TenantOnboardRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return onboard_tenant(
        db,
        onboard_data,
        current_user
    )


@router.get(
    "/{tenant_id}",
    response_model=TenantResponse
)
def get_tenant_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    ensure_platform_admin(
        db,
        current_user
    )

    return get_tenant_or_404(
        db,
        tenant_id
    )


@router.put(
    "/{tenant_id}",
    response_model=TenantResponse
)
def update_tenant_api(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return update_tenant(
        db,
        tenant_id,
        tenant_data,
        current_user
    )


@router.patch(
    "/{tenant_id}/suspend",
    response_model=TenantResponse
)
def suspend_tenant_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return suspend_tenant(
        db,
        tenant_id,
        current_user
    )


@router.patch(
    "/{tenant_id}/activate",
    response_model=TenantResponse
)
def activate_tenant_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return activate_tenant(
        db,
        tenant_id,
        current_user
    )


@router.post(
    "/{tenant_id}/admin",
    response_model=TenantOnboardingResponse,
    status_code=201
)
def create_tenant_admin_api(
    tenant_id: int,
    admin_data: TenantAdminCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_tenant_admin(
        db,
        tenant_id,
        admin_data,
        current_user
    )


@router.get(
    "/{tenant_id}/onboarding-status",
    response_model=TenantOnboardingResponse
)
def get_onboarding_status_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return get_onboarding_status(
        db,
        tenant_id,
        current_user
    )


@router.get(
    "/{tenant_id}/collaboration/settings",
    response_model=TenantCollaborationSettingsResponse
)
def get_collaboration_settings_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return get_collaboration_settings(
        db,
        tenant_id,
        current_user
    )


@router.put(
    "/{tenant_id}/collaboration/settings",
    response_model=TenantCollaborationSettingsResponse
)
def update_collaboration_settings_api(
    tenant_id: int,
    settings_data: TenantCollaborationSettingsUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return update_collaboration_settings(
        db,
        tenant_id,
        settings_data,
        current_user
    )


@router.get(
    "/{tenant_id}/collaboration/usage",
    response_model=TenantCollaborationUsageResponse
)
def get_collaboration_usage_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return get_collaboration_usage(
        db,
        tenant_id,
        current_user
    )


@router.post(
    "/{tenant_id}/collaboration/recalculate-usage",
    response_model=TenantCollaborationUsageResponse
)
def recalculate_collaboration_usage_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return recalculate_collaboration_usage(
        db,
        tenant_id,
        current_user
    )
