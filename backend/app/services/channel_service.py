from app.utils.db_exceptions import (
    handle_db_commit
)

from fastapi import HTTPException

from sqlalchemy import func, select

from sqlalchemy.orm import Session

from app.models.collaboration_model import (
    Channel,
    ChannelMember,
    TenantCollaborationSettings,
    Workspace,
    WorkspaceMember
)

from app.schemas.channel_schema import (
    ChannelCreate,
    ChannelUpdate
)

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.tenant_service import (
    create_default_collaboration_settings,
    refresh_collaboration_usage
)

from app.services.workspace_service import (
    WORKSPACE_MANAGER_ROLES,
    WORKSPACE_MEMBER_MANAGER_ROLES,
    ensure_active_tenant_user,
    ensure_workspace_access,
    get_active_workspace_member,
    get_workspace_or_404
)


CHANNEL_MANAGER_TYPES = [
    "PRIVATE",
    "ANNOUNCEMENT"
]


def get_channel_or_404(
    db: Session,
    channel_id: int
):

    channel = db.execute(
        select(Channel).where(
            Channel.id == channel_id
        )
    ).scalar_one_or_none()

    if not channel:

        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return channel


def get_channel_member(
    db: Session,
    channel_id: int,
    user_id: int
):

    return db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id
        )
    ).scalar_one_or_none()


def ensure_channel_manager_access(
    db: Session,
    workspace,
    current_user
):

    if workspace.tenant_id != current_user.organization_id:

        raise HTTPException(
            status_code=403,
            detail="Cross-tenant channel access is blocked"
        )

    if current_user.role in WORKSPACE_MANAGER_ROLES:

        return

    workspace_member = get_active_workspace_member(
        db,
        workspace.id,
        current_user.id
    )

    if (
        workspace_member
        and
        workspace_member.role in WORKSPACE_MEMBER_MANAGER_ROLES
    ):

        return

    raise HTTPException(
        status_code=403,
        detail="Not authorized to manage channels"
    )


def ensure_channel_access(
    db: Session,
    channel,
    current_user
):

    if channel.tenant_id != current_user.organization_id:

        raise HTTPException(
            status_code=403,
            detail="Cross-tenant channel access is blocked"
        )

    workspace = get_workspace_or_404(
        db,
        channel.workspace_id
    )

    ensure_workspace_access(
        db,
        workspace,
        current_user
    )

    if channel.channel_type not in CHANNEL_MANAGER_TYPES:

        return

    if current_user.role in WORKSPACE_MANAGER_ROLES:

        return

    channel_member = get_channel_member(
        db,
        channel.id,
        current_user.id
    )

    if channel_member:

        return

    raise HTTPException(
        status_code=403,
        detail="Private channel access is restricted"
    )


def ensure_channel_limit_available(
    db: Session,
    workspace
):

    settings = db.execute(
        select(TenantCollaborationSettings).where(
            TenantCollaborationSettings.tenant_id == workspace.tenant_id
        )
    ).scalar_one_or_none()

    if not settings:

        settings = create_default_collaboration_settings(
            db,
            workspace.tenant_id
        )

    if not settings.channel_enabled:

        raise HTTPException(
            status_code=403,
            detail="Channel module is disabled for this tenant"
        )

    active_channel_count = db.execute(
        select(func.count(Channel.id)).where(
            Channel.workspace_id == workspace.id,
            Channel.is_archived == False
        )
    ).scalar() or 0

    if active_channel_count >= settings.max_channels_per_workspace:

        raise HTTPException(
            status_code=400,
            detail="Channel limit reached for this workspace"
        )


def ensure_channel_name_available(
    db: Session,
    workspace_id: int,
    name: str,
    channel_id: int | None = None
):

    existing_channel = db.execute(
        select(Channel).where(
            Channel.workspace_id == workspace_id,
            Channel.name == name
        )
    ).scalar_one_or_none()

    if existing_channel and existing_channel.id != channel_id:

        raise HTTPException(
            status_code=400,
            detail="Channel name already exists in this workspace"
        )


def create_channel(
    db: Session,
    channel_data: ChannelCreate,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    workspace = get_workspace_or_404(
        db,
        channel_data.workspace_id
    )

    if workspace.is_archived:

        raise HTTPException(
            status_code=400,
            detail="Cannot create channel in archived workspace"
        )

    ensure_channel_manager_access(
        db,
        workspace,
        current_user
    )

    ensure_channel_limit_available(
        db,
        workspace
    )

    ensure_channel_name_available(
        db,
        workspace.id,
        channel_data.name
    )

    channel = Channel(
        tenant_id=workspace.tenant_id,
        workspace_id=workspace.id,
        name=channel_data.name,
        description=channel_data.description,
        channel_type=channel_data.channel_type,
        created_by=current_user.id,
        is_archived=False
    )

    db.add(channel)

    db.flush()

    db.add(
        ChannelMember(
            channel_id=channel.id,
            user_id=current_user.id,
            is_muted=False
        )
    )

    refresh_collaboration_usage(
        db,
        workspace.tenant_id
    )

    create_audit_log(
        db,
        current_user.id,
        "created channel",
        "channel",
        channel.id,
        module_name="channel",
        action_type="created",
        record_id=channel.id
    )

    handle_db_commit(db)

    db.refresh(channel)

    return channel


def get_workspace_channels_statement(
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

    statement = select(Channel).where(
        Channel.workspace_id == workspace.id
    )

    if current_user.role not in WORKSPACE_MANAGER_ROLES:

        joined_channel_ids = select(
            ChannelMember.channel_id
        ).where(
            ChannelMember.user_id == current_user.id
        )

        statement = statement.where(
            (
                Channel.channel_type.notin_(
                    CHANNEL_MANAGER_TYPES
                )
            )
            |
            (
                Channel.id.in_(joined_channel_ids)
            )
        )

    return statement.order_by(
        Channel.created_at.desc()
    )


def get_channel_by_id(
    db: Session,
    channel_id: int,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    channel = get_channel_or_404(
        db,
        channel_id
    )

    ensure_channel_access(
        db,
        channel,
        current_user
    )

    return channel


def update_channel(
    db: Session,
    channel_id: int,
    channel_data: ChannelUpdate,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    channel = get_channel_or_404(
        db,
        channel_id
    )

    workspace = get_workspace_or_404(
        db,
        channel.workspace_id
    )

    ensure_channel_manager_access(
        db,
        workspace,
        current_user
    )

    ensure_channel_name_available(
        db,
        workspace.id,
        channel_data.name,
        channel_id=channel.id
    )

    channel.name = channel_data.name

    channel.description = channel_data.description

    channel.channel_type = channel_data.channel_type

    create_audit_log(
        db,
        current_user.id,
        "updated channel",
        "channel",
        channel.id,
        module_name="channel",
        action_type="updated",
        record_id=channel.id
    )

    handle_db_commit(db)

    db.refresh(channel)

    return channel


def archive_channel(
    db: Session,
    channel_id: int,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    channel = get_channel_or_404(
        db,
        channel_id
    )

    workspace = get_workspace_or_404(
        db,
        channel.workspace_id
    )

    ensure_channel_manager_access(
        db,
        workspace,
        current_user
    )

    channel.is_archived = True

    refresh_collaboration_usage(
        db,
        channel.tenant_id
    )

    create_audit_log(
        db,
        current_user.id,
        "archived channel",
        "channel",
        channel.id,
        module_name="channel",
        action_type="archived",
        record_id=channel.id
    )

    handle_db_commit(db)

    db.refresh(channel)

    return channel


def restore_channel(
    db: Session,
    channel_id: int,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    channel = get_channel_or_404(
        db,
        channel_id
    )

    workspace = get_workspace_or_404(
        db,
        channel.workspace_id
    )

    ensure_channel_manager_access(
        db,
        workspace,
        current_user
    )

    if channel.is_archived:

        ensure_channel_limit_available(
            db,
            workspace
        )

    channel.is_archived = False

    refresh_collaboration_usage(
        db,
        channel.tenant_id
    )

    create_audit_log(
        db,
        current_user.id,
        "restored channel",
        "channel",
        channel.id,
        module_name="channel",
        action_type="restored",
        record_id=channel.id
    )

    handle_db_commit(db)

    db.refresh(channel)

    return channel


def join_channel(
    db: Session,
    channel_id: int,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    channel = get_channel_or_404(
        db,
        channel_id
    )

    if channel.is_archived:

        raise HTTPException(
            status_code=400,
            detail="Cannot join archived channel"
        )

    workspace = get_workspace_or_404(
        db,
        channel.workspace_id
    )

    ensure_workspace_access(
        db,
        workspace,
        current_user
    )

    if channel.channel_type in CHANNEL_MANAGER_TYPES:

        if current_user.role not in WORKSPACE_MANAGER_ROLES:

            raise HTTPException(
                status_code=403,
                detail="Private or announcement channel access is restricted"
            )

    existing_member = get_channel_member(
        db,
        channel.id,
        current_user.id
    )

    if existing_member:

        return existing_member

    member = ChannelMember(
        channel_id=channel.id,
        user_id=current_user.id,
        is_muted=False
    )

    db.add(member)

    create_audit_log(
        db,
        current_user.id,
        "joined channel",
        "channel_member",
        channel.id,
        module_name="channel",
        action_type="joined",
        record_id=channel.id
    )

    handle_db_commit(db)

    db.refresh(member)

    return member


def leave_channel(
    db: Session,
    channel_id: int,
    current_user
):

    ensure_active_tenant_user(
        db,
        current_user
    )

    channel = get_channel_or_404(
        db,
        channel_id
    )

    ensure_channel_access(
        db,
        channel,
        current_user
    )

    member = get_channel_member(
        db,
        channel.id,
        current_user.id
    )

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Channel member not found"
        )

    create_audit_log(
        db,
        current_user.id,
        "left channel",
        "channel_member",
        channel.id,
        module_name="channel",
        action_type="left",
        record_id=channel.id
    )

    db.delete(member)

    handle_db_commit(db)

    return member
