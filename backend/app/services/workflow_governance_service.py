from app.utils.db_exceptions import (
    handle_db_commit
)

from datetime import datetime

from fastapi import HTTPException

from sqlalchemy import and_, or_, select

from sqlalchemy.orm import Session

from app.models.approval_model import Approval

from app.models.task_model import Task

from app.models.user_model import User

from app.models.workflow_governance_model import (
    ApprovalDelegation,
    ApprovalEscalation,
    NotificationPreference
)

from app.schemas.workflow_governance_schema import (
    ApprovalDelegationCreate,
    ApprovalEscalationCreate,
    NotificationPreferenceUpdate
)

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.notification_service import (
    create_notification
)


def get_current_time():

    return datetime.utcnow()


def ensure_manager_or_admin(
    current_user
):

    if current_user.role not in [
        "admin",
        "manager"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )


def ensure_same_organization(
    current_user,
    target_user
):

    if (
        current_user.organization_id
        and
        target_user.organization_id != current_user.organization_id
    ):

        raise HTTPException(
            status_code=403,
            detail="User must belong to your organization"
        )


def get_user_or_404(
    db: Session,
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

    return user


def get_approval_or_404(
    db: Session,
    approval_id: int
):

    approval = db.execute(
        select(Approval).where(
            Approval.id == approval_id
        )
    ).scalar_one_or_none()

    if not approval:

        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    return approval


def approval_write_visible_to_user(
    db: Session,
    approval,
    current_user
):

    if current_user.role == "admin":

        if not current_user.organization_id:

            return True

        organization_user_ids = select(User.id).where(
            User.organization_id == current_user.organization_id
        )

        if approval.requested_by in db.execute(
            organization_user_ids
        ).scalars().all():

            return True

        if not approval.task_id:

            return False

    if current_user.role == "manager":

        if approval.requested_by == current_user.id:

            return True

        if approval.reviewed_by == current_user.id:

            return True

    if not approval.task_id:

        return current_user.role == "admin"

    task = db.execute(
        select(Task).where(
            Task.id == approval.task_id
        )
    ).scalar_one_or_none()

    if not task:

        return False

    if current_user.role == "admin":

        if not current_user.organization_id:

            return True

        organization_user_ids = db.execute(
            select(User.id).where(
                User.organization_id == current_user.organization_id
            )
        ).scalars().all()

        return (
            task.created_by in organization_user_ids
            or
            task.assigned_to in organization_user_ids
        )

    if current_user.role == "manager":

        return (
            task.created_by == current_user.id
            or
            task.assigned_to == current_user.id
        )

    return False


def get_approval_escalation_visibility_conditions(
    current_user
):

    if current_user.role == "admin":

        if not current_user.organization_id:

            return []

        organization_user_ids = select(User.id).where(
            User.organization_id == current_user.organization_id
        )

        return [
            or_(
                Approval.requested_by.in_(
                    organization_user_ids
                ),
                Approval.reviewed_by.in_(
                    organization_user_ids
                ),
                Task.created_by.in_(
                    organization_user_ids
                ),
                Task.assigned_to.in_(
                    organization_user_ids
                )
            )
        ]

    if current_user.role == "auditor":

        organization_user_ids = select(User.id).where(
            User.organization_id == current_user.organization_id
        )

        return [
            or_(
                Approval.requested_by.in_(
                    organization_user_ids
                ),
                Approval.reviewed_by.in_(
                    organization_user_ids
                ),
                Task.created_by.in_(
                    organization_user_ids
                ),
                Task.assigned_to.in_(
                    organization_user_ids
                )
            )
        ]

    if current_user.role == "manager":

        return [
            or_(
                ApprovalEscalation.escalated_from == current_user.id,
                ApprovalEscalation.escalated_to == current_user.id,
                Approval.requested_by == current_user.id,
                Approval.reviewed_by == current_user.id,
                Task.created_by == current_user.id,
                Task.assigned_to == current_user.id
            )
        ]

    return [
        ApprovalEscalation.id == -1
    ]


def get_approval_escalations_statement(
    current_user
):

    statement = select(ApprovalEscalation).join(
        Approval,
        ApprovalEscalation.approval_id == Approval.id
    ).outerjoin(
        Task,
        Approval.task_id == Task.id
    )

    conditions = get_approval_escalation_visibility_conditions(
        current_user
    )

    if conditions:

        statement = statement.where(
            *conditions
        )

    return statement.order_by(
        ApprovalEscalation.escalated_at.desc()
    )


def get_pending_approval_escalations_statement(
    current_user
):

    return get_approval_escalations_statement(
        current_user
    ).where(
        ApprovalEscalation.status == "pending"
    )


def get_approval_escalation_or_404(
    db: Session,
    escalation_id: int
):

    escalation = db.execute(
        select(ApprovalEscalation).where(
            ApprovalEscalation.id == escalation_id
        )
    ).scalar_one_or_none()

    if not escalation:

        raise HTTPException(
            status_code=404,
            detail="Approval escalation not found"
        )

    return escalation


def get_escalation_history_statement(
    approval_id: int,
    current_user
):

    return get_approval_escalations_statement(
        current_user
    ).where(
        ApprovalEscalation.approval_id == approval_id
    )


def create_approval_escalation(
    db: Session,
    escalation_data: ApprovalEscalationCreate,
    current_user
):

    ensure_manager_or_admin(
        current_user
    )

    if current_user.role != "manager":

        raise HTTPException(
            status_code=403,
            detail="Only Manager can escalate approval to Admin"
        )

    approval = get_approval_or_404(
        db,
        escalation_data.approval_id
    )

    if approval.requested_by == current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Managers cannot escalate their own approval requests"
        )

    if approval.current_level == "completed":

        raise HTTPException(
            status_code=400,
            detail="Completed approval cannot be escalated"
        )

    if approval.current_level != "manager":

        raise HTTPException(
            status_code=400,
            detail="Only manager-level approvals can be escalated"
        )

    if not approval_write_visible_to_user(
        db,
        approval,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    escalated_to_user = get_user_or_404(
        db,
        escalation_data.escalated_to
    )

    ensure_same_organization(
        current_user,
        escalated_to_user
    )

    if escalated_to_user.role != "admin":

        raise HTTPException(
            status_code=400,
            detail="Manager-level approvals can be escalated only to Admin"
        )

    existing_pending = db.execute(
        select(ApprovalEscalation).where(
            ApprovalEscalation.approval_id == approval.id,
            ApprovalEscalation.status == "pending"
        )
    ).scalar_one_or_none()

    if existing_pending:

        raise HTTPException(
            status_code=400,
            detail="Approval already has a pending escalation"
        )

    escalation_count = db.execute(
        select(ApprovalEscalation).where(
            ApprovalEscalation.approval_id == approval.id
        )
    ).scalars().all()

    escalation = ApprovalEscalation(
        approval_id=approval.id,
        escalated_from=current_user.id,
        escalated_to=escalation_data.escalated_to,
        reason=escalation_data.reason,
        escalation_level=len(escalation_count) + 1,
        status="pending"
    )

    db.add(escalation)

    approval.is_escalated = True

    approval.current_escalation_to = escalation_data.escalated_to

    approval.current_level = "admin"

    db.flush()

    create_audit_log(
        db,
        current_user.id,
        "escalated approval",
        "approval_escalation",
        escalation.id,
        module_name="approval",
        action_type="escalated",
        record_id=approval.id
    )

    create_notification(
        db,
        escalation_data.escalated_to,
        f"Approval #{approval.id} was escalated to you.",
        notification_type="escalation",
        priority="high"
    )

    handle_db_commit(db)

    db.refresh(escalation)

    return escalation


def resolve_approval_escalation(
    db: Session,
    escalation_id: int,
    current_user
):

    ensure_manager_or_admin(
        current_user
    )

    escalation = get_approval_escalation_or_404(
        db,
        escalation_id
    )

    if escalation.status != "pending":

        raise HTTPException(
            status_code=400,
            detail="Escalation already resolved or cancelled"
        )

    escalation.status = "resolved"

    escalation.resolved_at = get_current_time()

    approval = get_approval_or_404(
        db,
        escalation.approval_id
    )

    if not approval_write_visible_to_user(
        db,
        approval,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    approval.is_escalated = False

    approval.current_escalation_to = None

    create_audit_log(
        db,
        current_user.id,
        "resolved approval escalation",
        "approval_escalation",
        escalation.id,
        module_name="approval",
        action_type="resolved",
        record_id=approval.id
    )

    create_notification(
        db,
        escalation.escalated_from,
        f"Escalation #{escalation.id} for approval #{approval.id} was resolved.",
        notification_type="escalation",
        priority="medium"
    )

    handle_db_commit(db)

    db.refresh(escalation)

    return escalation


def cancel_approval_escalation(
    db: Session,
    escalation_id: int,
    current_user
):

    ensure_manager_or_admin(
        current_user
    )

    escalation = get_approval_escalation_or_404(
        db,
        escalation_id
    )

    if escalation.status != "pending":

        raise HTTPException(
            status_code=400,
            detail="Escalation already resolved or cancelled"
        )

    escalation.status = "cancelled"

    escalation.resolved_at = get_current_time()

    approval = get_approval_or_404(
        db,
        escalation.approval_id
    )

    if not approval_write_visible_to_user(
        db,
        approval,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    approval.is_escalated = False

    approval.current_escalation_to = None

    create_audit_log(
        db,
        current_user.id,
        "cancelled approval escalation",
        "approval_escalation",
        escalation.id,
        module_name="approval",
        action_type="cancelled",
        record_id=approval.id
    )

    handle_db_commit(db)

    db.refresh(escalation)

    return escalation


def get_approval_delegation_or_404(
    db: Session,
    delegation_id: int
):

    delegation = db.execute(
        select(ApprovalDelegation).where(
            ApprovalDelegation.id == delegation_id
        )
    ).scalar_one_or_none()

    if not delegation:

        raise HTTPException(
            status_code=404,
            detail="Approval delegation not found"
        )

    return delegation


def create_approval_delegation(
    db: Session,
    delegation_data: ApprovalDelegationCreate,
    current_user
):

    ensure_manager_or_admin(
        current_user
    )

    delegatee = get_user_or_404(
        db,
        delegation_data.delegatee_id
    )

    ensure_same_organization(
        current_user,
        delegatee
    )

    if delegatee.id == current_user.id:

        raise HTTPException(
            status_code=400,
            detail="Delegator and delegatee cannot be the same user"
        )

    if delegatee.role not in [
        "admin",
        "manager"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Approvals can be delegated only to Manager or Admin"
        )

    if delegatee.role != current_user.role:

        raise HTTPException(
            status_code=400,
            detail="Approvals can be delegated only to the same role"
        )

    overlapping_delegation = db.execute(
        select(ApprovalDelegation).where(
            ApprovalDelegation.delegator_id == current_user.id,
            ApprovalDelegation.is_active == True,
            ApprovalDelegation.start_date <= delegation_data.end_date,
            ApprovalDelegation.end_date >= delegation_data.start_date
        )
    ).scalar_one_or_none()

    if overlapping_delegation:

        raise HTTPException(
            status_code=400,
            detail="Delegation date conflict"
        )

    delegation = ApprovalDelegation(
        delegator_id=current_user.id,
        delegatee_id=delegation_data.delegatee_id,
        start_date=delegation_data.start_date,
        end_date=delegation_data.end_date,
        reason=delegation_data.reason,
        is_active=True
    )

    db.add(delegation)

    db.flush()

    create_audit_log(
        db,
        current_user.id,
        "created approval delegation",
        "approval_delegation",
        delegation.id,
        module_name="approval",
        action_type="delegated",
        record_id=delegation.id
    )

    create_notification(
        db,
        delegation_data.delegatee_id,
        f"{current_user.name} delegated approvals to you.",
        notification_type="approval",
        priority="medium"
    )

    handle_db_commit(db)

    db.refresh(delegation)

    return delegation


def get_my_delegations_statement(
    current_user
):

    return select(ApprovalDelegation).where(
        or_(
            ApprovalDelegation.delegator_id == current_user.id,
            ApprovalDelegation.delegatee_id == current_user.id
        )
    ).order_by(
        ApprovalDelegation.created_at.desc()
    )


def get_active_delegations_statement(
    db: Session,
    current_user
):

    now = get_current_time()

    statement = select(ApprovalDelegation).where(
        ApprovalDelegation.is_active == True,
        ApprovalDelegation.start_date <= now,
        ApprovalDelegation.end_date >= now
    )

    if current_user.organization_id:

        organization_user_ids = select(User.id).where(
            User.organization_id == current_user.organization_id
        )

        statement = statement.where(
            ApprovalDelegation.delegator_id.in_(
                organization_user_ids
            )
        )

    return statement.order_by(
        ApprovalDelegation.created_at.desc()
    )


def cancel_approval_delegation(
    db: Session,
    delegation_id: int,
    current_user
):

    delegation = get_approval_delegation_or_404(
        db,
        delegation_id
    )

    if (
        current_user.role != "admin"
        and
        delegation.delegator_id != current_user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="Only delegator or admin can cancel delegation"
        )

    delegation.is_active = False

    create_audit_log(
        db,
        current_user.id,
        "cancelled approval delegation",
        "approval_delegation",
        delegation.id,
        module_name="approval",
        action_type="cancelled_delegation",
        record_id=delegation.id
    )

    handle_db_commit(db)

    db.refresh(delegation)

    return delegation


def user_has_active_delegation_from(
    db: Session,
    delegatee_id: int,
    delegator_id: int
):

    now = get_current_time()

    delegation = db.execute(
        select(ApprovalDelegation).where(
            ApprovalDelegation.delegatee_id == delegatee_id,
            ApprovalDelegation.delegator_id == delegator_id,
            ApprovalDelegation.is_active == True,
            ApprovalDelegation.start_date <= now,
            ApprovalDelegation.end_date >= now
        )
    ).scalar_one_or_none()

    return delegation is not None


def get_notification_preference_for_user(
    db: Session,
    user_id: int
):

    return db.execute(
        select(NotificationPreference).where(
            NotificationPreference.user_id == user_id
        )
    ).scalar_one_or_none()


def create_default_notification_preferences(
    db: Session,
    user_id: int,
    current_user=None
):

    user = get_user_or_404(
        db,
        user_id
    )

    preference = get_notification_preference_for_user(
        db,
        user_id
    )

    if preference:

        return preference

    preference = NotificationPreference(
        user_id=user.id,
        in_app_enabled=True,
        email_enabled=False,
        task_notifications=True,
        approval_notifications=True,
        escalation_notifications=True,
        document_notifications=True
    )

    db.add(preference)

    db.flush()

    if current_user:

        create_audit_log(
            db,
            current_user.id,
            "created notification preferences",
            "notification_preference",
            preference.id,
            module_name="notification",
            action_type="created_preferences",
            record_id=preference.id
        )

    handle_db_commit(db)

    db.refresh(preference)

    return preference


def get_my_notification_preferences(
    db: Session,
    current_user
):

    return create_default_notification_preferences(
        db,
        current_user.id
    )


def update_my_notification_preferences(
    db: Session,
    preference_data: NotificationPreferenceUpdate,
    current_user
):

    preference = create_default_notification_preferences(
        db,
        current_user.id
    )

    preference.in_app_enabled = preference_data.in_app_enabled

    preference.email_enabled = preference_data.email_enabled

    preference.task_notifications = preference_data.task_notifications

    preference.approval_notifications = preference_data.approval_notifications

    preference.escalation_notifications = preference_data.escalation_notifications

    preference.document_notifications = preference_data.document_notifications

    create_audit_log(
        db,
        current_user.id,
        "updated notification preferences",
        "notification_preference",
        preference.id,
        module_name="notification",
        action_type="updated_preferences",
        record_id=preference.id
    )

    handle_db_commit(db)

    db.refresh(preference)

    return preference


def notification_allowed_for_user(
    db: Session,
    user_id: int,
    notification_type: str | None
):

    preference = get_notification_preference_for_user(
        db,
        user_id
    )

    if not preference:

        return True

    if not preference.in_app_enabled:

        return False

    if notification_type == "task":

        return preference.task_notifications

    if notification_type == "approval":

        return preference.approval_notifications

    if notification_type == "escalation":

        return preference.escalation_notifications

    if notification_type == "document":

        return preference.document_notifications

    return True
