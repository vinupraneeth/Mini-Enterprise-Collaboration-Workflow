from app.utils.db_exceptions import (
    handle_db_commit
)

from datetime import datetime, timedelta

from fastapi import HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.models.approval_model import Approval

from app.models.task_model import Task

from app.models.user_model import User

from app.models.workflow_governance_model import (
    SLARule,
    SLATracking
)

from app.schemas.sla_schema import (
    SLARuleCreate,
    SLARuleUpdate
)

from app.services.audit_log_service import (
    create_audit_log
)


SLA_STATUS_ACTIVE = "active"
SLA_STATUS_BREACHED = "breached"
SLA_STATUS_COMPLETED = "completed_within_sla"


def get_current_time():

    return datetime.utcnow()


def normalize_sla_value(
    value
):

    return str(value).strip().lower()


def get_organization_user_ids(
    db: Session,
    current_user
):

    if not current_user.organization_id:

        return []

    return db.execute(
        select(User.id).where(
            User.organization_id == current_user.organization_id
        )
    ).scalars().all()


def task_visible_for_sla(
    db: Session,
    task: Task,
    current_user
):

    if current_user.role in [
        "admin",
        "auditor"
    ]:

        if not current_user.organization_id:

            return True

        organization_user_ids = get_organization_user_ids(
            db,
            current_user
        )

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


def approval_visible_for_sla(
    db: Session,
    approval: Approval,
    current_user
):

    if current_user.role in [
        "admin",
        "auditor"
    ]:

        if not current_user.organization_id:

            return True

        organization_user_ids = get_organization_user_ids(
            db,
            current_user
        )

        if approval.requested_by in organization_user_ids:

            return True

        if approval.reviewed_by in organization_user_ids:

            return True

        if approval.task_id:

            task = db.execute(
                select(Task).where(
                    Task.id == approval.task_id
                )
            ).scalar_one_or_none()

            if task:

                return task_visible_for_sla(
                    db,
                    task,
                    current_user
                )

        return False

    if current_user.role == "manager":

        if approval.requested_by == current_user.id:

            return True

        if approval.reviewed_by == current_user.id:

            return True

        if not approval.task_id:

            return False

        task = db.execute(
            select(Task).where(
                Task.id == approval.task_id
            )
        ).scalar_one_or_none()

        if not task:

            return False

        return task_visible_for_sla(
            db,
            task,
            current_user
        )

    return False


def sla_tracking_visible_to_user(
    db: Session,
    tracking: SLATracking,
    current_user
):

    if tracking.module_name == "task":

        task = db.execute(
            select(Task).where(
                Task.id == tracking.record_id
            )
        ).scalar_one_or_none()

        if not task:

            return False

        return task_visible_for_sla(
            db,
            task,
            current_user
        )

    if tracking.module_name == "approval":

        approval = db.execute(
            select(Approval).where(
                Approval.id == tracking.record_id
            )
        ).scalar_one_or_none()

        if not approval:

            return False

        return approval_visible_for_sla(
            db,
            approval,
            current_user
        )

    return current_user.role == "admin"


def get_sla_rules_statement():

    return select(SLARule).order_by(
        SLARule.created_at.desc()
    )


def get_sla_rule_by_id(
    db: Session,
    rule_id: int
):

    rule = db.execute(
        select(SLARule).where(
            SLARule.id == rule_id
        )
    ).scalar_one_or_none()

    if not rule:

        raise HTTPException(
            status_code=404,
            detail="SLA rule not found"
        )

    return rule


def create_sla_rule(
    db: Session,
    rule_data: SLARuleCreate,
    current_user
):

    rule = SLARule(
        module_name=normalize_sla_value(
            rule_data.module_name
        ),
        priority=normalize_sla_value(
            rule_data.priority
        ),
        allowed_hours=rule_data.allowed_hours,
        escalation_enabled=rule_data.escalation_enabled,
        escalation_after_hours=rule_data.escalation_after_hours,
        is_active=rule_data.is_active,
        created_by=current_user.id
    )

    db.add(rule)

    db.flush()

    create_audit_log(
        db,
        current_user.id,
        "created SLA rule",
        "sla_rule",
        rule.id,
        module_name="sla",
        action_type="created",
        record_id=rule.id
    )

    handle_db_commit(db)

    db.refresh(rule)

    return rule


def update_sla_rule(
    db: Session,
    rule_id: int,
    rule_data: SLARuleUpdate,
    current_user
):

    rule = get_sla_rule_by_id(
        db,
        rule_id
    )

    rule.module_name = normalize_sla_value(
        rule_data.module_name
    )

    rule.priority = normalize_sla_value(
        rule_data.priority
    )

    rule.allowed_hours = rule_data.allowed_hours

    rule.escalation_enabled = rule_data.escalation_enabled

    rule.escalation_after_hours = rule_data.escalation_after_hours

    rule.is_active = rule_data.is_active

    create_audit_log(
        db,
        current_user.id,
        "updated SLA rule",
        "sla_rule",
        rule.id,
        module_name="sla",
        action_type="updated",
        record_id=rule.id
    )

    handle_db_commit(db)

    db.refresh(rule)

    return rule


def disable_sla_rule(
    db: Session,
    rule_id: int,
    current_user
):

    rule = get_sla_rule_by_id(
        db,
        rule_id
    )

    rule.is_active = False

    create_audit_log(
        db,
        current_user.id,
        "disabled SLA rule",
        "sla_rule",
        rule.id,
        module_name="sla",
        action_type="disabled",
        record_id=rule.id
    )

    handle_db_commit(db)

    return rule


def find_active_sla_rule(
    db: Session,
    module_name: str,
    priority: str
):

    return db.execute(
        select(SLARule).where(
            SLARule.module_name == normalize_sla_value(
                module_name
            ),
            SLARule.priority == normalize_sla_value(
                priority
            ),
            SLARule.is_active == True
        ).order_by(
            SLARule.id.desc()
        )
    ).scalar_one_or_none()


def get_existing_sla_tracking(
    db: Session,
    module_name: str,
    record_id: int
):

    return db.execute(
        select(SLATracking).where(
            SLATracking.module_name == normalize_sla_value(
                module_name
            ),
            SLATracking.record_id == record_id,
            SLATracking.status.in_(
                [
                    SLA_STATUS_ACTIVE,
                    SLA_STATUS_BREACHED
                ]
            )
        ).order_by(
            SLATracking.id.desc()
        )
    ).scalar_one_or_none()


def create_sla_tracking(
    db: Session,
    module_name: str,
    record_id: int,
    rule: SLARule
):

    now = get_current_time()

    tracking = SLATracking(
        module_name=normalize_sla_value(
            module_name
        ),
        record_id=record_id,
        sla_rule_id=rule.id,
        start_time=now,
        due_time=now + timedelta(
            hours=rule.allowed_hours
        ),
        status=SLA_STATUS_ACTIVE
    )

    db.add(tracking)

    return tracking


def apply_sla_to_task_if_available(
    db: Session,
    task: Task
):

    if get_existing_sla_tracking(
        db,
        "task",
        task.id
    ):

        return None

    rule = find_active_sla_rule(
        db,
        "task",
        task.priority
    )

    if not rule:

        return None

    tracking = create_sla_tracking(
        db,
        "task",
        task.id,
        rule
    )

    task.sla_status = tracking.status

    task.sla_due_time = tracking.due_time

    task.is_sla_breached = False

    return tracking


def get_approval_priority(
    db: Session,
    approval: Approval
):

    if not approval.task_id:

        return "medium"

    task = db.execute(
        select(Task).where(
            Task.id == approval.task_id
        )
    ).scalar_one_or_none()

    if not task:

        return "medium"

    return task.priority


def apply_sla_to_approval_if_available(
    db: Session,
    approval: Approval
):

    if get_existing_sla_tracking(
        db,
        "approval",
        approval.id
    ):

        return None

    priority = get_approval_priority(
        db,
        approval
    )

    rule = find_active_sla_rule(
        db,
        "approval",
        priority
    )

    if not rule:

        return None

    tracking = create_sla_tracking(
        db,
        "approval",
        approval.id,
        rule
    )

    approval.sla_status = tracking.status

    approval.sla_due_time = tracking.due_time

    return tracking


def start_task_sla_tracking(
    db: Session,
    task_id: int,
    current_user
):

    task = db.execute(
        select(Task).where(
            Task.id == task_id
        )
    ).scalar_one_or_none()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if not task_visible_for_sla(
        db,
        task,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    existing_tracking = get_existing_sla_tracking(
        db,
        "task",
        task.id
    )

    if existing_tracking:

        raise HTTPException(
            status_code=400,
            detail="SLA tracking is already active for this task"
        )

    rule = find_active_sla_rule(
        db,
        "task",
        task.priority
    )

    if not rule:

        raise HTTPException(
            status_code=404,
            detail="Matching SLA rule not found"
        )

    tracking = create_sla_tracking(
        db,
        "task",
        task.id,
        rule
    )

    task.sla_status = tracking.status

    task.sla_due_time = tracking.due_time

    task.is_sla_breached = False

    create_audit_log(
        db,
        current_user.id,
        "started task SLA tracking",
        "sla_tracking",
        task.id,
        module_name="sla",
        action_type="started",
        record_id=task.id
    )

    handle_db_commit(db)

    db.refresh(tracking)

    return tracking


def start_approval_sla_tracking(
    db: Session,
    approval_id: int,
    current_user
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

    if not approval_visible_for_sla(
        db,
        approval,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    existing_tracking = get_existing_sla_tracking(
        db,
        "approval",
        approval.id
    )

    if existing_tracking:

        raise HTTPException(
            status_code=400,
            detail="SLA tracking is already active for this approval"
        )

    priority = get_approval_priority(
        db,
        approval
    )

    rule = find_active_sla_rule(
        db,
        "approval",
        priority
    )

    if not rule:

        raise HTTPException(
            status_code=404,
            detail="Matching SLA rule not found"
        )

    tracking = create_sla_tracking(
        db,
        "approval",
        approval.id,
        rule
    )

    approval.sla_status = tracking.status

    approval.sla_due_time = tracking.due_time

    create_audit_log(
        db,
        current_user.id,
        "started approval SLA tracking",
        "sla_tracking",
        approval.id,
        module_name="sla",
        action_type="started",
        record_id=approval.id
    )

    handle_db_commit(db)

    db.refresh(tracking)

    return tracking


def update_record_sla_status(
    db: Session,
    tracking: SLATracking
):

    if tracking.module_name == "task":

        task = db.execute(
            select(Task).where(
                Task.id == tracking.record_id
            )
        ).scalar_one_or_none()

        if task:

            task.sla_status = tracking.status

            task.sla_due_time = tracking.due_time

            task.is_sla_breached = (
                tracking.status == SLA_STATUS_BREACHED
            )

    if tracking.module_name == "approval":

        approval = db.execute(
            select(Approval).where(
                Approval.id == tracking.record_id
            )
        ).scalar_one_or_none()

        if approval:

            approval.sla_status = tracking.status

            approval.sla_due_time = tracking.due_time


def refresh_sla_breach_status(
    db: Session,
    tracking: SLATracking
):

    if tracking.status != SLA_STATUS_ACTIVE:

        return tracking

    now = get_current_time()

    if tracking.due_time >= now:

        return tracking

    tracking.status = SLA_STATUS_BREACHED

    tracking.breach_reason = (
        f"SLA due time crossed at {tracking.due_time}"
    )

    update_record_sla_status(
        db,
        tracking
    )

    return tracking


def complete_sla_tracking_record(
    db: Session,
    tracking: SLATracking
):

    if tracking.completed_time:

        return tracking

    now = get_current_time()

    tracking.completed_time = now

    if now <= tracking.due_time:

        tracking.status = SLA_STATUS_COMPLETED

        tracking.breach_reason = None

    else:

        tracking.status = SLA_STATUS_BREACHED

        tracking.breach_reason = "SLA was completed after due time"

    update_record_sla_status(
        db,
        tracking
    )

    return tracking


def complete_sla_tracking(
    db: Session,
    tracking_id: int,
    current_user
):

    tracking = get_sla_tracking_by_id(
        db,
        tracking_id
    )

    if not sla_tracking_visible_to_user(
        db,
        tracking,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if tracking.completed_time:

        raise HTTPException(
            status_code=400,
            detail="SLA already completed"
        )

    complete_sla_tracking_record(
        db,
        tracking
    )

    create_audit_log(
        db,
        current_user.id,
        "completed SLA tracking",
        "sla_tracking",
        tracking.id,
        module_name="sla",
        action_type="completed",
        record_id=tracking.id
    )

    handle_db_commit(db)

    db.refresh(tracking)

    return tracking


def complete_sla_for_record(
    db: Session,
    module_name: str,
    record_id: int
):

    tracking = get_existing_sla_tracking(
        db,
        module_name,
        record_id
    )

    if not tracking:

        return None

    return complete_sla_tracking_record(
        db,
        tracking
    )


def get_sla_tracking_by_id(
    db: Session,
    tracking_id: int
):

    tracking = db.execute(
        select(SLATracking).where(
            SLATracking.id == tracking_id
        )
    ).scalar_one_or_none()

    if not tracking:

        raise HTTPException(
            status_code=404,
            detail="SLA tracking record not found"
        )

    return refresh_sla_breach_status(
        db,
        tracking
    )


def get_active_sla_tracking_statement():

    return select(SLATracking).where(
        SLATracking.status == SLA_STATUS_ACTIVE
    ).order_by(
        SLATracking.due_time.asc()
    )


def get_breached_sla_tracking_statement():

    return select(SLATracking).where(
        SLATracking.status == SLA_STATUS_BREACHED
    ).order_by(
        SLATracking.due_time.asc()
    )


def get_completed_sla_tracking_statement():

    return select(SLATracking).where(
        SLATracking.status == SLA_STATUS_COMPLETED
    ).order_by(
        SLATracking.completed_time.desc()
    )


def fetch_active_sla_tracking(
    db: Session,
    current_user
):

    records = db.execute(
        get_active_sla_tracking_statement()
    ).scalars().all()

    for record in records:

        refresh_sla_breach_status(
            db,
            record
        )

    handle_db_commit(db)

    return [
        record
        for record in records
        if (
            record.status == SLA_STATUS_ACTIVE
            and
            sla_tracking_visible_to_user(
                db,
                record,
                current_user
            )
        )
    ]


def fetch_breached_sla_tracking(
    db: Session,
    current_user
):

    active_records = db.execute(
        get_active_sla_tracking_statement()
    ).scalars().all()

    for record in active_records:

        refresh_sla_breach_status(
            db,
            record
        )

    handle_db_commit(db)

    records = db.execute(
        get_breached_sla_tracking_statement()
    ).scalars().all()

    return [
        record
        for record in records
        if sla_tracking_visible_to_user(
            db,
            record,
            current_user
        )
    ]


def fetch_completed_sla_tracking(
    db: Session,
    current_user
):

    records = db.execute(
        get_completed_sla_tracking_statement()
    ).scalars().all()

    return [
        record
        for record in records
        if sla_tracking_visible_to_user(
            db,
            record,
            current_user
        )
    ]


def fetch_sla_tracking_for_module(
    db: Session,
    module_name: str,
    current_user
):

    records = db.execute(
        select(SLATracking).where(
            SLATracking.module_name == normalize_sla_value(
                module_name
            )
        ).order_by(
            SLATracking.due_time.asc()
        )
    ).scalars().all()

    for record in records:

        refresh_sla_breach_status(
            db,
            record
        )

    handle_db_commit(db)

    return [
        record
        for record in records
        if sla_tracking_visible_to_user(
            db,
            record,
            current_user
        )
    ]


def fetch_sla_tracking_for_record(
    db: Session,
    module_name: str,
    record_id: int,
    current_user
):

    tracking = db.execute(
        select(SLATracking).where(
            SLATracking.module_name == normalize_sla_value(
                module_name
            ),
            SLATracking.record_id == record_id
        ).order_by(
            SLATracking.id.desc()
        )
    ).scalar_one_or_none()

    if not tracking:

        raise HTTPException(
            status_code=404,
            detail="SLA tracking record not found"
        )

    refresh_sla_breach_status(
        db,
        tracking
    )

    if not sla_tracking_visible_to_user(
        db,
        tracking,
        current_user
    ):

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    handle_db_commit(db)

    return tracking
