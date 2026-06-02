from sqlalchemy import select

from app.models.audit_log_model import AuditLog


def create_audit_log(
    db,
    user_id,
    action,
    entity,
    entity_id=None
):

    audit_log = AuditLog(

        user_id=user_id,

        action=action,

        entity=entity,

        entity_id=entity_id
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
