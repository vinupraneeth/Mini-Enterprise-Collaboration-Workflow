import asyncio

import json

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.active_connections = {}

        self.loop = None


    async def connect(
        self,
        user_id: int,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections[user_id] = websocket

        self.loop = asyncio.get_running_loop()


    def disconnect(
        self,
        user_id: int
    ):

        self.active_connections.pop(
            user_id,
            None
        )


    async def receive(
        self,
        websocket: WebSocket
    ):

        await websocket.receive_text()


    async def send_message(
        self,
        user_id: int,
        message
    ):

        websocket = self.active_connections.get(
            user_id
        )

        if not websocket:

            return

        if not isinstance(
            message,
            str
        ):

            message = json.dumps(
                message,
                default=str
            )

        await websocket.send_text(
            message
        )


    async def broadcast_to_users(
        self,
        user_ids,
        message
    ):

        for user_id in set(user_ids):

            await self.send_message(
                user_id,
                message
            )


manager = ConnectionManager()
