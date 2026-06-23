from app.utils.db_exceptions import (
    handle_db_commit
)

import re

from fastapi import HTTPException

from sqlalchemy import func, select

from sqlalchemy.orm import Session

from app.models.collaboration_model import (
    TenantCollaborationSettings,
    Workspace,
    WorkspaceMember
)

from app.models.saas_model import (
    Organization
)

from app.models.user_model import (
    User
)

from app.schemas.workspace_schema import (
    WorkspaceCreate,
    WorkspaceMemberCreate,
    WorkspaceMemberRoleUpdate,
    WorkspaceUpdate
)

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.tenant_service import (
    create_default_collaboration_settings,
    refresh_collaboration_usage
)


WORKSPACE_MANAGER_ROLES = [
    "admin",
    "manager"
]

WORKSPACE_MEMBER_MANAGER_ROLES = [
    "WORKSPACE_ADMIN",
    "MODERATOR"
]


def slugify(
    value: str
):

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        value.lower()
    ).strip("-")

    return slug or "workspace"


def ensure_active_tenant_user(
    db: Session,
    current_user
):

    if not current_user.organization_id:

        raise HTTPException(
            status_code=403,
            detail="User must belong to a tenant"
        )

    tenant = db.execute(
        select(Organization).where(
            Organization.id == current_user.organization_id
        )
    ).scalar_one_or_none()

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    if tenant.status == "SUSPENDED":

        raise HTTPException(
            status_code=403,
            detail="Tenant is suspended"
        )

    return tenant


def ensure_workspace_manager(
    current_user
):

    if current_user.role not in WORKSPACE_MANAGER_ROLES:

        raise HTTPException(
            status_code=403,
            detail="Only Admin or Manager can manage workspaces"
        )


def generate_unique_workspace_slug(
    db: Session,
    tenant_id: int,
    name: str,
    requested_slug: str | None = None
):

    base_slug = slugify(
        requested_slug or name
    )

    slug = base_slug

    counter = 2

    while db.execute(
        select(Workspace).where(
            Workspace.tenant_id == tenant_id,
            Workspace.slug == slug
        )
    ).scalar_one_or_none():

        slug = f"{base_slug}-{counter}"

        counter += 1

    return slug


def get_workspace_or_404(
    db: Session,
    workspace_id: int
):

    workspace = db.execute(
        select(Workspace).where(
            Workspace.id == workspace_id
        )
    ).scalar_one_or_none()

    if not workspace:

        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return workspace


def user_is_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int
):

    member = db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.is_active == True
        )
    ).scalar_one_or_none()

    return member is not None


def ensure_workspace_access(
    db: Session,
    workspace,
    current_user
):

    if workspace.tenant_id != current_user.organization_id:

        raise HTTPException(
            status_code=403,
            detail="Cross-tenant workspace access is blocked"
        )

    if workspace.visibility == "PUBLIC":

        return

    if current_user.role in WORKSPACE_MANAGER_ROLES:

        return

    if user_is_workspace_member(
        db,
        workspace.id,
        current_user.id
    ):

        return

    raise HTTPException(
        status_code=403,
        detail="Private workspace access is restricted"
    )


def ensure_workspace_write_access(
    db: Session,
    workspace,
    current_user
):

    if workspace.tenant_id != current_user.organization_id:

        raise HTTPException(
            status_code=403,
            detail="Cross-tenant workspace access is blocked"
        )

    ensure_workspace_manager(
        current_user
    )


def get_active_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int
):

    return db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.is_active == True
        )
    ).scalar_one_or_none()


def ensure_workspace_member_manage_access(
    db: Session,
    workspace,
    current_user
):

    if workspace.tenant_id != current_user.organization_id:

        raise HTTPException(
            status_code=403,
            detail="Cross-tenant workspace access is blocked"
        )

    if current_user.role in WORKSPACE_MANAGER_ROLES:

        return

    active_member = get_active_workspace_member(
        db,
        workspace.id,
        current_user.id
    )

    if (
        active_member
        and
        active_member.role in WORKSPACE_MEMBER_MANAGER_ROLES
    ):

        return

    raise HTTPException(
        status_code=403,
        detail="Not authorized to manage workspace members"
    )


def get_tenant_user_or_404(
    db: Session,
    tenant_id: int,
    user_id: int
):

    user = db.execute(
        select(User).where(
            User.id == user_id
        )
    ).scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.organization_id != tenant_id:

        raise HTTPException(
            status_code=403,
            detail="Workspace members must belong to the same tenant"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=400,
            detail="Inactive users cannot be added to workspace"
        )

    return user


def ensure_workspace_member_limit_available(
    db: Session,
    workspace
):

    settings = create_default_collaboration_settings(
        db,
        workspace.tenant_id
    )

    active_member_count = db.execute(
        select(func.count(WorkspaceMember.id)).where(
            WorkspaceMember.workspace_id == workspace.id,
            WorkspaceMember.is_active == True
        )
    ).scalar() or 0

    if active_member_count >= settings.max_workspace_members:

        raise HTTPException(
            status_code=400,
            detail="Workspace member limit reached"
        )


def get_visible_workspaces_statement(
    db: Session,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    statement = select(Workspace).where(
        Workspace.tenant_id == current_user.organization_id
    )

    if current_user.role not in WORKSPACE_MANAGER_ROLES:

        member_workspace_ids = select(
            WorkspaceMember.workspace_id
        ).where(
            WorkspaceMember.user_id == current_user.id,
            WorkspaceMember.is_active == True
        )

        statement = statement.where(
            (
                Workspace.visibility == "PUBLIC"
            )
            |
            (
                Workspace.id.in_(member_workspace_ids)
            )
        )

    return statement.order_by(
        Workspace.created_at.desc()
    )


def create_workspace(
    db: Session,
    workspace_data: WorkspaceCreate,
    current_user
):

    tenant = ensure_active_tenant_user(
        db,
        current_user
    )

    ensure_workspace_manager(
        current_user
    )

    settings = create_default_collaboration_settings(
        db,
        tenant.id
    )

    if not settings.workspace_enabled:

        raise HTTPException(
            status_code=403,
            detail="Workspace module is disabled for this tenant"
        )

    active_workspace_count = db.execute(
        select(func.count(Workspace.id)).where(
            Workspace.tenant_id == tenant.id,
            Workspace.is_archived == False
        )
    ).scalar() or 0

    if active_workspace_count >= settings.max_workspaces:

        raise HTTPException(
            status_code=400,
            detail="Workspace limit reached for this tenant"
        )

    slug = generate_unique_workspace_slug(
        db,
        tenant.id,
        workspace_data.name,
        workspace_data.slug
    )

    workspace = Workspace(
        tenant_id=tenant.id,
        name=workspace_data.name,
        slug=slug,
        description=workspace_data.description,
        avatar_url=workspace_data.avatar_url,
        visibility=workspace_data.visibility,
        created_by=current_user.id,
        is_archived=False
    )

    db.add(workspace)

    db.flush()

    db.add(
        WorkspaceMember(
            workspace_id=workspace.id,
            user_id=current_user.id,
            role="WORKSPACE_ADMIN",
            is_active=True
        )
    )

    refresh_collaboration_usage(
        db,
        tenant.id
    )

    create_audit_log(
        db,
        current_user.id,
        "created workspace",
        "workspace",
        workspace.id,
        module_name="workspace",
        action_type="created",
        record_id=workspace.id
    )

    handle_db_commit(db)

    db.refresh(workspace)

    return workspace


def get_workspace_by_id(
    db: Session,
    workspace_id: int,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_access(
        db,
        workspace,
        current_user
    )

    return workspace


def update_workspace(
    db: Session,
    workspace_id: int,
    workspace_data: WorkspaceUpdate,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_write_access(
        db,
        workspace,
        current_user
    )

    workspace.name = workspace_data.name

    workspace.description = workspace_data.description

    workspace.avatar_url = workspace_data.avatar_url

    workspace.visibility = workspace_data.visibility

    if (
        workspace_data.slug
        and
        workspace_data.slug != workspace.slug
    ):

        workspace.slug = generate_unique_workspace_slug(
            db,
            workspace.tenant_id,
            workspace_data.name,
            workspace_data.slug
        )

    create_audit_log(
        db,
        current_user.id,
        "updated workspace",
        "workspace",
        workspace.id,
        module_name="workspace",
        action_type="updated",
        record_id=workspace.id
    )

    handle_db_commit(db)

    db.refresh(workspace)

    return workspace


def archive_workspace(
    db: Session,
    workspace_id: int,
    current_user
):

    tenant = ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_write_access(
        db,
        workspace,
        current_user
    )

    workspace.is_archived = True

    refresh_collaboration_usage(
        db,
        tenant.id
    )

    create_audit_log(
        db,
        current_user.id,
        "archived workspace",
        "workspace",
        workspace.id,
        module_name="workspace",
        action_type="archived",
        record_id=workspace.id
    )

    handle_db_commit(db)

    db.refresh(workspace)

    return workspace


def restore_workspace(
    db: Session,
    workspace_id: int,
    current_user
):

    tenant = ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_write_access(
        db,
        workspace,
        current_user
    )

    settings = db.execute(
        select(TenantCollaborationSettings).where(
            TenantCollaborationSettings.tenant_id == tenant.id
        )
    ).scalar_one_or_none()

    if not settings:

        settings = create_default_collaboration_settings(
            db,
            tenant.id
        )

    active_workspace_count = db.execute(
        select(func.count(Workspace.id)).where(
            Workspace.tenant_id == tenant.id,
            Workspace.is_archived == False
        )
    ).scalar() or 0

    if (
        workspace.is_archived
        and
        active_workspace_count >= settings.max_workspaces
    ):

        raise HTTPException(
            status_code=400,
            detail="Workspace limit reached for this tenant"
        )

    workspace.is_archived = False

    refresh_collaboration_usage(
        db,
        tenant.id
    )

    create_audit_log(
        db,
        current_user.id,
        "restored workspace",
        "workspace",
        workspace.id,
        module_name="workspace",
        action_type="restored",
        record_id=workspace.id
    )

    handle_db_commit(db)

    db.refresh(workspace)

    return workspace


def add_workspace_member(
    db: Session,
    workspace_id: int,
    member_data: WorkspaceMemberCreate,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_member_manage_access(
        db,
        workspace,
        current_user
    )

    if workspace.is_archived:

        raise HTTPException(
            status_code=400,
            detail="Archived workspace cannot accept new members"
        )

    get_tenant_user_or_404(
        db,
        workspace.tenant_id,
        member_data.user_id
    )

    existing_member = db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace.id,
            WorkspaceMember.user_id == member_data.user_id
        )
    ).scalar_one_or_none()

    if existing_member and existing_member.is_active:

        raise HTTPException(
            status_code=400,
            detail="Workspace member already exists"
        )

    if existing_member:

        ensure_workspace_member_limit_available(
            db,
            workspace
        )

        existing_member.role = member_data.role

        existing_member.is_active = True

        member = existing_member

    else:

        ensure_workspace_member_limit_available(
            db,
            workspace
        )

        member = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=member_data.user_id,
            role=member_data.role,
            is_active=True
        )

        db.add(member)

    db.flush()

    refresh_collaboration_usage(
        db,
        workspace.tenant_id
    )

    create_audit_log(
        db,
        current_user.id,
        "added workspace member",
        "workspace_member",
        member.id,
        module_name="workspace",
        action_type="added_member",
        record_id=workspace.id
    )

    handle_db_commit(db)

    db.refresh(member)

    return member


def get_workspace_members_statement(
    db: Session,
    workspace_id: int,
    search: str | None,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_access(
        db,
        workspace,
        current_user
    )

    statement = select(WorkspaceMember).join(
        User,
        WorkspaceMember.user_id == User.id
    ).where(
        WorkspaceMember.workspace_id == workspace.id,
        WorkspaceMember.is_active == True
    )

    if search:

        search_value = f"%{search.strip()}%"

        statement = statement.where(
            (
                User.name.like(search_value)
            )
            |
            (
                User.email.like(search_value)
            )
        )

    return statement.order_by(
        WorkspaceMember.joined_at.desc()
    )


def update_workspace_member_role(
    db: Session,
    workspace_id: int,
    user_id: int,
    role_data: WorkspaceMemberRoleUpdate,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_member_manage_access(
        db,
        workspace,
        current_user
    )

    member = get_active_workspace_member(
        db,
        workspace.id,
        user_id
    )

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Workspace member not found"
        )

    member.role = role_data.role

    create_audit_log(
        db,
        current_user.id,
        "updated workspace member role",
        "workspace_member",
        member.id,
        module_name="workspace",
        action_type="updated_member_role",
        record_id=workspace.id
    )

    handle_db_commit(db)

    db.refresh(member)

    return member


def remove_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        workspace_id
    )

    ensure_workspace_member_manage_access(
        db,
        workspace,
        current_user
    )

    member = get_active_workspace_member(
        db,
        workspace.id,
        user_id
    )

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Workspace member not found"
        )

    member.is_active = False

    refresh_collaboration_usage(
        db,
        workspace.tenant_id
    )

    create_audit_log(
        db,
        current_user.id,
        "removed workspace member",
        "workspace_member",
        member.id,
        module_name="workspace",
        action_type="removed_member",
        record_id=workspace.id
    )

    handle_db_commit(db)

    db.refresh(member)

    return member
