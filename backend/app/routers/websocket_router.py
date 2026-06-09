from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from app.services.websocket_manager import (
    manager
)


router = APIRouter(
    tags=["WebSocket"]
)


@router.websocket(
    "/ws/{user_id}"
)
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int
):

    await manager.connect(
        user_id,
        websocket
    )

    try:

        while True:

            await manager.receive(
                websocket
            )

    except WebSocketDisconnect:

        manager.disconnect(
            user_id
        )
