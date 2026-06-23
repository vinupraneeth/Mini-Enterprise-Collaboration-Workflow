from fastapi import (
    APIRouter,
    Depends
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user
)

from app.db.deps import get_db

from app.schemas.channel_schema import (
    ChannelCreate,
    ChannelMemberResponse,
    ChannelResponse,
    ChannelUpdate
)

from app.services.channel_service import (
    archive_channel,
    create_channel,
    get_channel_by_id,
    get_workspace_channels_statement,
    join_channel,
    leave_channel,
    restore_channel,
    update_channel
)


router = APIRouter(
    tags=["Channels"]
)


@router.post(
    "/channels",
    response_model=ChannelResponse,
    status_code=201
)
def create_channel_api(
    channel_data: ChannelCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return create_channel(
        db,
        channel_data,
        current_user
    )


@router.get(
    "/workspaces/{workspace_id}/channels",
    response_model=Page[ChannelResponse]
)
def get_workspace_channels_api(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return paginate(
        db,
        get_workspace_channels_statement(
            db,
            workspace_id,
            current_user
        )
    )


@router.get(
    "/channels/{channel_id}",
    response_model=ChannelResponse
)
def get_channel_api(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_channel_by_id(
        db,
        channel_id,
        current_user
    )


@router.put(
    "/channels/{channel_id}",
    response_model=ChannelResponse
)
def update_channel_api(
    channel_id: int,
    channel_data: ChannelUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return update_channel(
        db,
        channel_id,
        channel_data,
        current_user
    )


@router.patch(
    "/channels/{channel_id}/archive",
    response_model=ChannelResponse
)
def archive_channel_api(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return archive_channel(
        db,
        channel_id,
        current_user
    )


@router.patch(
    "/channels/{channel_id}/restore",
    response_model=ChannelResponse
)
def restore_channel_api(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return restore_channel(
        db,
        channel_id,
        current_user
    )


@router.post(
    "/channels/{channel_id}/join",
    response_model=ChannelMemberResponse
)
def join_channel_api(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return join_channel(
        db,
        channel_id,
        current_user
    )


@router.post(
    "/channels/{channel_id}/leave",
    response_model=ChannelMemberResponse
)
def leave_channel_api(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return leave_channel(
        db,
        channel_id,
        current_user
    )
