from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page, paginate

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.core.dependencies import (
    get_current_user
)

from app.schemas.task_comment_schema import (
    TaskCommentCreate,
    TaskCommentResponse
)

from app.services.task_comment_service import (
    add_comment_to_task,
    fetch_task_comments
)


router = APIRouter(

    prefix="/tasks",

    tags=["Task Comments"]
)


@router.post(

    "/{task_id}/comments",

    response_model=TaskCommentResponse,

    status_code=201
)
def create_comment_api(

    task_id: int,

    comment_data: TaskCommentCreate,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return add_comment_to_task(

        db,

        task_id,

        comment_data,

        current_user
    )


@router.get(

    "/{task_id}/comments",

    response_model=Page[
        TaskCommentResponse
    ]
)
def get_comments_api(

    task_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    return paginate(

        fetch_task_comments(

            db,

            task_id,

            current_user
        )
    )
