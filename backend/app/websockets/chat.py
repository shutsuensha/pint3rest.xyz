from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .manager import manager


def register_websocket(app: FastAPI):
    @app.websocket("/ws/{chat_id}/{user_id}")
    async def chat_endpoint(websocket: WebSocket, chat_id: int, user_id: int):
        await manager.connect(websocket, chat_id, user_id)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.send_message(data, chat_id, user_id)
        except WebSocketDisconnect:
            manager.disconnect(chat_id, user_id)