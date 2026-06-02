from pathlib import Path

from fastapi import HTTPException, UploadFile

from sqlalchemy import func, select

from sqlalchemy.orm import Session

from app.models.document_model import Document

from app.models.task_model import Task

from app.services.audit_log_service import (
    create_audit_log
)

from app.services.notification_service import (
    create_notification
)


UPLOAD_ROOT = Path("uploads")


def check_document_task_access(
    task,
    current_user
):

    if current_user.role == "admin":

        return

    if current_user.role == "manager":

        if (
            task.created_by == current_user.id
            or
            task.assigned_to == current_user.id
        ):

            return

    if current_user.role == "employee" and task.assigned_to == current_user.id:

        return

    raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )


def get_task_or_404(
    db: Session,
    task_id: int
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

    return task


def validate_file(
    file: UploadFile
):

    allowed_extensions = {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".png",
        ".jpg",
        ".jpeg",
        ".txt"
    }

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )


def get_next_document_version(
    db: Session,
    task_id: int,
    file_name: str
):

    latest_version = db.execute(
        select(
            func.max(Document.version)
        ).where(
            Document.task_id == task_id,
            Document.file_name == file_name
        )
    ).scalar_one()

    return (
        latest_version or 0
    ) + 1


def upload_document(
    db: Session,
    task_id: int,
    file: UploadFile,
    current_user
):

    task = get_task_or_404(
        db,
        task_id
    )

    check_document_task_access(
        task,
        current_user
    )

    validate_file(file)

    file_name = Path(
        file.filename or "document"
    ).name

    version = get_next_document_version(
        db,
        task_id,
        file_name
    )

    task_folder = UPLOAD_ROOT / f"task_{task_id}"

    task_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    stored_name = f"v{version}_{file_name}"

    file_path = task_folder / stored_name

    with file_path.open("wb") as output_file:

        output_file.write(
            file.file.read()
        )

    document = Document(

        file_name=file_name,

        file_path=str(file_path),

        version=version,

        uploaded_by=current_user.id,

        task_id=task_id
    )

    db.add(document)

    db.flush()

    create_audit_log(
        db,
        current_user.id,
        "uploaded document",
        "document",
        document.id
    )

    message = (
        f"Document '{document.file_name}' uploaded for task #{task_id}."
    )

    notified_users = set()

    if task.created_by and task.created_by != current_user.id:

        create_notification(
            db,
            task.created_by,
            message
        )

        notified_users.add(task.created_by)

    if (
        task.assigned_to
        and
        task.assigned_to != current_user.id
        and
        task.assigned_to not in notified_users
    ):

        create_notification(
            db,
            task.assigned_to,
            message
        )

    db.commit()

    db.refresh(document)

    return document


def fetch_document_by_id(
    db: Session,
    document_id: int,
    current_user
):

    document = db.execute(
        select(Document).where(
            Document.id == document_id
        )
    ).scalar_one_or_none()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    task = get_task_or_404(
        db,
        document.task_id
    )

    check_document_task_access(
        task,
        current_user
    )

    return document


def fetch_documents_by_task(
    db: Session,
    task_id: int,
    current_user
):

    task = get_task_or_404(
        db,
        task_id
    )

    check_document_task_access(
        task,
        current_user
    )

    return db.execute(
        get_documents_by_task_statement(
            db,
            task_id,
            current_user
        )
    ).scalars().all()


def get_documents_by_task_statement(
    db: Session,
    task_id: int,
    current_user
):

    task = get_task_or_404(
        db,
        task_id
    )

    check_document_task_access(
        task,
        current_user
    )

    return select(Document).where(
        Document.task_id == task_id
    ).order_by(
        Document.created_at.desc()
    )
