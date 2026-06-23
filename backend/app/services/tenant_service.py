from app.utils.db_exceptions import (
    handle_db_commit
)

from datetime import datetime

import re

from fastapi import HTTPException

from sqlalchemy import func, select

from sqlalchemy.orm import Session

from app.models.collaboration_model import (
    Channel,
    TenantCollaborationSettings,
    TenantCollaborationUsage,
    TenantOnboarding,
    Workspace,
    WorkspaceMember
)

from app.models.saas_model import (
    Organization
)

from app.models.user_model import (
    User
)

from app.schemas.tenant_schema import (
    TenantCollaborationSettingsUpdate,
    TenantAdminCreate,
    TenantCreate,
    TenantOnboardRequest,
    TenantUpdate
)

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.saas_service import (
    DEFAULT_ORGANIZATION_SLUG
)

from app.utils.hashing import (
    hash_password
)


VALID_TENANT_STATUSES = [
    "ACTIVE",
    "SUSPENDED",
    "TRIAL",
    "CANCELLED"
]


def slugify(
    value: str
):

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        value.lower()
    ).strip("-")

    return slug or "tenant"


def ensure_platform_admin(
    db: Session,
    current_user
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only platform admin can manage tenants"
        )

    organization = None

    if current_user.organization_id:

        organization = db.execute(
            select(Organization).where(
                Organization.id == current_user.organization_id
            )
        ).scalar_one_or_none()

    if (
        organization
        and
        organization.slug == DEFAULT_ORGANIZATION_SLUG
    ):

        return current_user

    raise HTTPException(
        status_code=403,
        detail="Only platform admin can manage tenants"
    )


def is_platform_admin(
    db: Session,
    current_user
):

    if current_user.role != "admin":

        return False

    organization = None

    if current_user.organization_id:

        organization = db.execute(
            select(Organization).where(
                Organization.id == current_user.organization_id
            )
        ).scalar_one_or_none()

    return bool(
        organization
        and
        organization.slug == DEFAULT_ORGANIZATION_SLUG
    )


def ensure_tenant_admin_or_platform_admin(
    db: Session,
    tenant_id: int,
    current_user
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only tenant admin can access tenant collaboration settings"
        )

    if is_platform_admin(
        db,
        current_user
    ):

        return current_user

    if current_user.organization_id == tenant_id:

        return current_user

    raise HTTPException(
        status_code=403,
        detail="Not authorized for this tenant"
    )


def get_tenants_statement(
    db: Session,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    return select(Organization).order_by(
        Organization.created_at.desc()
    )


def get_tenant_or_404(
    db: Session,
    tenant_id: int
):

    tenant = db.execute(
        select(Organization).where(
            Organization.id == tenant_id
        )
    ).scalar_one_or_none()

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return tenant


def ensure_unique_tenant_identity(
    db: Session,
    contact_email: str,
    slug: str,
    tenant_id: int | None = None
):

    duplicate_email = db.execute(
        select(Organization).where(
            Organization.contact_email == contact_email
        )
    ).scalar_one_or_none()

    if duplicate_email and duplicate_email.id != tenant_id:

        raise HTTPException(
            status_code=400,
            detail="Tenant contact email already exists"
        )

    duplicate_slug = db.execute(
        select(Organization).where(
            Organization.slug == slug
        )
    ).scalar_one_or_none()

    if duplicate_slug and duplicate_slug.id != tenant_id:

        raise HTTPException(
            status_code=400,
            detail="Tenant slug already exists"
        )


def generate_unique_slug(
    db: Session,
    name: str,
    requested_slug: str | None = None
):

    base_slug = slugify(
        requested_slug or name
    )

    slug = base_slug

    counter = 2

    while db.execute(
        select(Organization).where(
            Organization.slug == slug
        )
    ).scalar_one_or_none():

        slug = f"{base_slug}-{counter}"

        counter += 1

    return slug


def create_default_collaboration_settings(
    db: Session,
    tenant_id: int
):

    settings = db.execute(
        select(TenantCollaborationSettings).where(
            TenantCollaborationSettings.tenant_id == tenant_id
        )
    ).scalar_one_or_none()

    if settings:

        return settings

    settings = TenantCollaborationSettings(
        tenant_id=tenant_id,
        max_workspaces=5,
        max_channels_per_workspace=10,
        max_workspace_members=50,
        max_storage_mb=1024,
        workspace_enabled=True,
        channel_enabled=True
    )

    db.add(settings)

    return settings


def get_collaboration_settings(
    db: Session,
    tenant_id: int,
    current_user
):

    ensure_tenant_admin_or_platform_admin(
        db,
        tenant_id,
        current_user
    )

    get_tenant_or_404(
        db,
        tenant_id
    )

    settings = create_default_collaboration_settings(
        db,
        tenant_id
    )

    handle_db_commit(db)

    db.refresh(settings)

    return settings


def update_collaboration_settings(
    db: Session,
    tenant_id: int,
    settings_data: TenantCollaborationSettingsUpdate,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    get_tenant_or_404(
        db,
        tenant_id
    )

    settings = create_default_collaboration_settings(
        db,
        tenant_id
    )

    settings.max_workspaces = settings_data.max_workspaces

    settings.max_channels_per_workspace = (
        settings_data.max_channels_per_workspace
    )

    settings.max_workspace_members = settings_data.max_workspace_members

    settings.max_storage_mb = settings_data.max_storage_mb

    settings.workspace_enabled = settings_data.workspace_enabled

    settings.channel_enabled = settings_data.channel_enabled

    create_audit_log(
        db,
        current_user.id,
        "updated tenant collaboration settings",
        "tenant_collaboration_settings",
        settings.id,
        module_name="tenant",
        action_type="updated_collaboration_settings",
        record_id=tenant_id
    )

    handle_db_commit(db)

    db.refresh(settings)

    return settings


def create_default_collaboration_usage(
    db: Session,
    tenant_id: int
):

    usage = db.execute(
        select(TenantCollaborationUsage).where(
            TenantCollaborationUsage.tenant_id == tenant_id
        )
    ).scalar_one_or_none()

    if usage:

        return usage

    usage = TenantCollaborationUsage(
        tenant_id=tenant_id,
        workspace_count=0,
        channel_count=0,
        member_count=0,
        storage_used_mb=0,
        last_calculated_at=datetime.utcnow()
    )

    db.add(usage)

    return usage


def get_collaboration_usage(
    db: Session,
    tenant_id: int,
    current_user
):

    ensure_tenant_admin_or_platform_admin(
        db,
        tenant_id,
        current_user
    )

    get_tenant_or_404(
        db,
        tenant_id
    )

    usage = create_default_collaboration_usage(
        db,
        tenant_id
    )

    handle_db_commit(db)

    db.refresh(usage)

    return usage


def recalculate_collaboration_usage(
    db: Session,
    tenant_id: int,
    current_user
):

    ensure_tenant_admin_or_platform_admin(
        db,
        tenant_id,
        current_user
    )

    get_tenant_or_404(
        db,
        tenant_id
    )

    usage = refresh_collaboration_usage(
        db,
        tenant_id
    )

    create_audit_log(
        db,
        current_user.id,
        "recalculated tenant collaboration usage",
        "tenant_collaboration_usage",
        usage.id,
        module_name="tenant",
        action_type="recalculated_usage",
        record_id=tenant_id
    )

    handle_db_commit(db)

    db.refresh(usage)

    return usage


def get_or_create_onboarding_record(
    db: Session,
    tenant_id: int
):

    onboarding = db.execute(
        select(TenantOnboarding).where(
            TenantOnboarding.tenant_id == tenant_id
        )
    ).scalar_one_or_none()

    if onboarding:

        return onboarding

    onboarding = TenantOnboarding(
        tenant_id=tenant_id,
        onboarding_status="PENDING",
        default_workspace_created=False,
        settings_created=False
    )

    db.add(onboarding)

    return onboarding


def create_tenant(
    db: Session,
    tenant_data: TenantCreate,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    tenant = build_tenant_record(
        db,
        tenant_data
    )

    create_audit_log(
        db,
        current_user.id,
        "created tenant",
        "tenant",
        tenant.id,
        module_name="tenant",
        action_type="created",
        record_id=tenant.id
    )

    handle_db_commit(db)

    db.refresh(tenant)

    return tenant


def build_tenant_record(
    db: Session,
    tenant_data: TenantCreate
):

    slug = generate_unique_slug(
        db,
        tenant_data.name,
        tenant_data.slug
    )

    ensure_unique_tenant_identity(
        db,
        str(tenant_data.contact_email),
        slug
    )

    tenant = Organization(
        name=tenant_data.name,
        slug=slug,
        contact_email=str(tenant_data.contact_email),
        phone=tenant_data.phone,
        address=tenant_data.address,
        industry=tenant_data.industry,
        status="ACTIVE"
    )

    db.add(tenant)

    db.flush()

    return tenant


def update_tenant(
    db: Session,
    tenant_id: int,
    tenant_data: TenantUpdate,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    tenant = get_tenant_or_404(
        db,
        tenant_id
    )

    if tenant_data.status not in VALID_TENANT_STATUSES:

        raise HTTPException(
            status_code=400,
            detail="Invalid tenant status"
        )

    ensure_unique_tenant_identity(
        db,
        str(tenant_data.contact_email),
        tenant.slug,
        tenant_id=tenant.id
    )

    tenant.name = tenant_data.name

    tenant.contact_email = str(
        tenant_data.contact_email
    )

    tenant.phone = tenant_data.phone

    tenant.address = tenant_data.address

    tenant.industry = tenant_data.industry

    tenant.status = tenant_data.status

    create_audit_log(
        db,
        current_user.id,
        "updated tenant",
        "tenant",
        tenant.id,
        module_name="tenant",
        action_type="updated",
        record_id=tenant.id
    )

    handle_db_commit(db)

    db.refresh(tenant)

    return tenant


def suspend_tenant(
    db: Session,
    tenant_id: int,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    tenant = get_tenant_or_404(
        db,
        tenant_id
    )

    tenant.status = "SUSPENDED"

    create_audit_log(
        db,
        current_user.id,
        "suspended tenant",
        "tenant",
        tenant.id,
        module_name="tenant",
        action_type="suspended",
        record_id=tenant.id
    )

    handle_db_commit(db)

    db.refresh(tenant)

    return tenant


def activate_tenant(
    db: Session,
    tenant_id: int,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    tenant = get_tenant_or_404(
        db,
        tenant_id
    )

    tenant.status = "ACTIVE"

    create_audit_log(
        db,
        current_user.id,
        "activated tenant",
        "tenant",
        tenant.id,
        module_name="tenant",
        action_type="activated",
        record_id=tenant.id
    )

    handle_db_commit(db)

    db.refresh(tenant)

    return tenant


def create_tenant_admin(
    db: Session,
    tenant_id: int,
    admin_data: TenantAdminCreate,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    tenant = get_tenant_or_404(
        db,
        tenant_id
    )

    onboarding = build_tenant_admin_setup(
        db,
        tenant,
        admin_data
    )

    create_audit_log(
        db,
        current_user.id,
        "created tenant admin",
        "tenant_onboarding",
        onboarding.id,
        module_name="tenant",
        action_type="created_admin",
        record_id=tenant.id
    )

    handle_db_commit(db)

    db.refresh(onboarding)

    return onboarding


def ensure_admin_email_available(
    db: Session,
    admin_email: str
):

    existing_user = db.execute(
        select(User).where(
            User.email == admin_email
        )
    ).scalar_one_or_none()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Admin email already registered"
        )


def build_tenant_admin_setup(
    db: Session,
    tenant,
    admin_data: TenantAdminCreate
):

    ensure_admin_email_available(
        db,
        str(admin_data.admin_email)
    )

    admin_user = User(
        name=admin_data.admin_name,
        email=str(admin_data.admin_email),
        hashed_password=hash_password(
            admin_data.admin_password
        ),
        role="admin",
        organization_id=tenant.id,
        is_active=True
    )

    db.add(admin_user)

    db.flush()

    create_default_collaboration_settings(
        db,
        tenant.id
    )

    create_default_collaboration_usage(
        db,
        tenant.id
    )

    onboarding = get_or_create_onboarding_record(
        db,
        tenant.id
    )

    onboarding.admin_user_id = admin_user.id

    onboarding.settings_created = True

    default_workspace_created = False

    if admin_data.create_default_workspace:

        default_workspace_created = create_default_workspace(
            db,
            tenant,
            admin_user
        )

    onboarding.default_workspace_created = (
        onboarding.default_workspace_created
        or
        default_workspace_created
    )

    onboarding.onboarding_status = "COMPLETED"

    onboarding.completed_at = datetime.utcnow()

    db.flush()

    refresh_collaboration_usage(
        db,
        tenant.id
    )

    return onboarding


def create_default_workspace(
    db: Session,
    tenant,
    admin_user
):

    existing_workspace = db.execute(
        select(Workspace).where(
            Workspace.tenant_id == tenant.id,
            Workspace.slug == "general"
        )
    ).scalar_one_or_none()

    if existing_workspace:

        return False

    workspace = Workspace(
        tenant_id=tenant.id,
        name="General",
        slug="general",
        description="Default workspace for tenant collaboration.",
        visibility="PUBLIC",
        created_by=admin_user.id,
        is_archived=False
    )

    db.add(workspace)

    db.flush()

    db.add(
        WorkspaceMember(
            workspace_id=workspace.id,
            user_id=admin_user.id,
            role="WORKSPACE_ADMIN",
            is_active=True
        )
    )

    return True


def refresh_collaboration_usage(
    db: Session,
    tenant_id: int
):

    usage = create_default_collaboration_usage(
        db,
        tenant_id
    )

    usage.workspace_count = db.execute(
        select(func.count(Workspace.id)).where(
            Workspace.tenant_id == tenant_id,
            Workspace.is_archived == False
        )
    ).scalar() or 0

    usage.channel_count = db.execute(
        select(func.count(Channel.id)).where(
            Channel.tenant_id == tenant_id,
            Channel.is_archived == False
        )
    ).scalar() or 0

    usage.member_count = db.execute(
        select(func.count(WorkspaceMember.id)).join(
            Workspace,
            WorkspaceMember.workspace_id == Workspace.id
        ).where(
            Workspace.tenant_id == tenant_id,
            WorkspaceMember.is_active == True
        )
    ).scalar() or 0

    usage.last_calculated_at = datetime.utcnow()

    return usage


def onboard_tenant(
    db: Session,
    onboard_data: TenantOnboardRequest,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    tenant = build_tenant_record(
        db,
        TenantCreate(
            name=onboard_data.name,
            slug=onboard_data.slug,
            contact_email=onboard_data.contact_email,
            phone=onboard_data.phone,
            address=onboard_data.address,
            industry=onboard_data.industry
        )
    )

    admin_payload = TenantAdminCreate(
        admin_name=onboard_data.admin_name,
        admin_email=onboard_data.admin_email,
        admin_password=onboard_data.admin_password,
        create_default_workspace=onboard_data.create_default_workspace
    )

    onboarding = build_tenant_admin_setup(
        db,
        tenant,
        admin_payload
    )

    create_audit_log(
        db,
        current_user.id,
        "onboarded tenant",
        "tenant_onboarding",
        onboarding.id,
        module_name="tenant",
        action_type="onboarded",
        record_id=tenant.id
    )

    handle_db_commit(db)

    db.refresh(tenant)

    db.refresh(onboarding)

    return {
        "tenant": tenant,
        "onboarding": onboarding
    }


def get_onboarding_status(
    db: Session,
    tenant_id: int,
    current_user
):

    ensure_platform_admin(
        db,
        current_user
    )

    get_tenant_or_404(
        db,
        tenant_id
    )

    onboarding = db.execute(
        select(TenantOnboarding).where(
            TenantOnboarding.tenant_id == tenant_id
        )
    ).scalar_one_or_none()

    if not onboarding:

        onboarding = get_or_create_onboarding_record(
            db,
            tenant_id
        )

        handle_db_commit(db)

        db.refresh(onboarding)

    return onboarding
