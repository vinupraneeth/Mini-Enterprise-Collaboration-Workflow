from fastapi import (
    APIRouter,
    Depends,
    Query
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user
)

from app.db.deps import get_db

from app.schemas.workspace_schema import (
    WorkspaceCreate,
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
    WorkspaceMemberRoleUpdate,
    WorkspaceResponse,
    WorkspaceUpdate
)

from app.services.workspace_service import (
    add_workspace_member,
    archive_workspace,
    create_workspace,
    get_visible_workspaces_statement,
    get_workspace_members_statement,
    get_workspace_by_id,
    remove_workspace_member,
    restore_workspace,
    update_workspace_member_role,
    update_workspace
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


@router.post(
    "/",
    response_model=WorkspaceResponse,
    status_code=201
)
def create_workspace_api(
    workspace_data: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return create_workspace(
        db,
        workspace_data,
        current_user
    )


@router.get(
    "/",
    response_model=Page[WorkspaceResponse]
)
def get_workspaces_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return paginate(
        db,
        get_visible_workspaces_statement(
            db,
            current_user
        )
    )


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse
)
def get_workspace_api(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_workspace_by_id(
        db,
        workspace_id,
        current_user
    )


@router.put(
    "/{workspace_id}",
    response_model=WorkspaceResponse
)
def update_workspace_api(
    workspace_id: int,
    workspace_data: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return update_workspace(
        db,
        workspace_id,
        workspace_data,
        current_user
    )


@router.patch(
    "/{workspace_id}/archive",
    response_model=WorkspaceResponse
)
def archive_workspace_api(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return archive_workspace(
        db,
        workspace_id,
        current_user
    )


@router.patch(
    "/{workspace_id}/restore",
    response_model=WorkspaceResponse
)
def restore_workspace_api(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return restore_workspace(
        db,
        workspace_id,
        current_user
    )


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=201
)
def add_workspace_member_api(
    workspace_id: int,
    member_data: WorkspaceMemberCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return add_workspace_member(
        db,
        workspace_id,
        member_data,
        current_user
    )


@router.get(
    "/{workspace_id}/members",
    response_model=Page[WorkspaceMemberResponse]
)
def get_workspace_members_api(
    workspace_id: int,
    search: str | None = Query(
        default=None,
        max_length=100
    ),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return paginate(
        db,
        get_workspace_members_statement(
            db,
            workspace_id,
            search,
            current_user
        )
    )


@router.patch(
    "/{workspace_id}/members/{user_id}/role",
    response_model=WorkspaceMemberResponse
)
def update_workspace_member_role_api(
    workspace_id: int,
    user_id: int,
    role_data: WorkspaceMemberRoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return update_workspace_member_role(
        db,
        workspace_id,
        user_id,
        role_data,
        current_user
    )


@router.delete(
    "/{workspace_id}/members/{user_id}",
    response_model=WorkspaceMemberResponse
)
def remove_workspace_member_api(
    workspace_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return remove_workspace_member(
        db,
        workspace_id,
        user_id,
        current_user
    )
