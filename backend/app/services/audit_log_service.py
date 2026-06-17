from datetime import datetime

from fastapi import HTTPException

from sqlalchemy import select

from app.models.audit_log_model import AuditLog


def create_audit_log(
    db,
    user_id,
    action,
    entity,
    entity_id=None,
    module_name=None,
    action_type=None,
    record_id=None,
    old_data=None,
    new_data=None,
    ip_address=None,
    user_agent=None
):

    audit_log = AuditLog(

        user_id=user_id,

        action=action,

        entity=entity,

        entity_id=entity_id,

        module_name=module_name or entity,

        action_type=action_type or action,

        record_id=record_id or entity_id,

        old_data=old_data,

        new_data=new_data,

        ip_address=ip_address,

        user_agent=user_agent
    )

    db.add(audit_log)

    return audit_log


def fetch_audit_logs(
    db
):

    return db.execute(
        get_audit_logs_statement()
    ).scalars().all()


def get_audit_logs_statement():

    return select(AuditLog).order_by(
        AuditLog.timestamp.desc()
    )


def get_audit_log_by_id(
    db,
    log_id: int
):

    audit_log = db.execute(
        select(AuditLog).where(
            AuditLog.id == log_id
        )
    ).scalar_one_or_none()

    if not audit_log:

        raise HTTPException(
            status_code=404,
            detail="Audit log not found"
        )

    return audit_log


def get_audit_logs_by_module_statement(
    module_name: str
):

    return select(AuditLog).where(
        AuditLog.module_name == module_name
    ).order_by(
        AuditLog.timestamp.desc()
    )


def get_audit_logs_by_user_statement(
    user_id: int
):

    return select(AuditLog).where(
        AuditLog.user_id == user_id
    ).order_by(
        AuditLog.timestamp.desc()
    )


def get_audit_logs_by_date_range_statement(
    start_date: datetime,
    end_date: datetime
):

    if end_date < start_date:

        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    return select(AuditLog).where(
        AuditLog.timestamp >= start_date,
        AuditLog.timestamp <= end_date
    ).order_by(
        AuditLog.timestamp.desc()
    )
