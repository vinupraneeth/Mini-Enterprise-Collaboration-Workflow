from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)

from fastapi.responses import FileResponse

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user
)

from app.db.deps import get_db

from app.schemas.document_schema import (
    DocumentResponse
)

from app.services.document_service import (
    fetch_document_by_id,
    get_documents_by_task_statement,
    upload_document
)

from app.services.audit_log_service import (
    create_audit_log
)


router = APIRouter(

    prefix="/documents",

    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=201
)
def upload_document_api(

    task_id: int,

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return upload_document(
        db,
        task_id,
        file,
        current_user
    )


@router.get(
    "/{document_id}"
)
def download_document_api(

    document_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    document = fetch_document_by_id(
        db,
        document_id,
        current_user
    )

    path = Path(document.file_path)

    if not path.exists():

        raise HTTPException(
            status_code=404,
            detail="Document file not found"
        )

    create_audit_log(
        db,
        current_user.id,
        "downloaded document",
        "document",
        document.id
    )

    db.commit()

    return FileResponse(
        path,
        filename=document.file_name
    )


@router.get(
    "/task/{task_id}",
    response_model=Page[DocumentResponse]
)
def get_task_documents_api(

    task_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return paginate(
        db,
        get_documents_by_task_statement(
            db,
            task_id,
            current_user
        )
    )
