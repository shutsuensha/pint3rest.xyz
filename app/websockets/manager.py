from fastapi import WebSocket
from fastapi.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        self.chats = {}

    async def connect(
        self, websocket: WebSocket, chat_id: int, user_id: int, chat_connection: bool | None = None
    ):
        await websocket.accept()
        if chat_id not in self.chats:
            self.chats[chat_id] = {
                "user_1": {"user_id": None, "websocket": None},
                "user_2": {"user_id": None, "websocket": None},
                "chat_connections": {
                    "user_1": {"user_id": None, "websocket": None},
                    "user_2": {"user_id": None, "websocket": None},
                },
            }

        if chat_connection is not None:
            if self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] is None:
                self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] = user_id
                self.chats[chat_id]["chat_connections"]["user_1"]["websocket"] = websocket

                websocket1 = self.chats[chat_id]["chat_connections"]["user_2"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"online": True})
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": True})

            else:
                self.chats[chat_id]["chat_connections"]["user_2"]["user_id"] = user_id
                self.chats[chat_id]["chat_connections"]["user_2"]["websocket"] = websocket

                websocket1 = self.chats[chat_id]["chat_connections"]["user_1"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"online": True})
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": True})
        else:
            if self.chats[chat_id]["user_1"]["user_id"] is None:
                self.chats[chat_id]["user_1"]["user_id"] = user_id
                self.chats[chat_id]["user_1"]["websocket"] = websocket

                websocket1 = self.chats[chat_id]["user_2"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"online": True})
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": True})

            else:
                self.chats[chat_id]["user_2"]["user_id"] = user_id
                self.chats[chat_id]["user_2"]["websocket"] = websocket

                websocket1 = self.chats[chat_id]["user_1"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"online": True})
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": True})

    async def disconnect(self, chat_id: int, user_id: int, chat_connection: bool | None = None):
        if chat_connection is not None:
            if self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] == user_id:
                self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] = None
                self.chats[chat_id]["chat_connections"]["user_1"]["websocket"] = None

                websocket = self.chats[chat_id]["chat_connections"]["user_2"]["websocket"]
                if websocket is not None:
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": False})

            if self.chats[chat_id]["chat_connections"]["user_2"]["user_id"] == user_id:
                self.chats[chat_id]["chat_connections"]["user_2"]["user_id"] = None
                self.chats[chat_id]["chat_connections"]["user_2"]["websocket"] = None

                websocket = self.chats[chat_id]["chat_connections"]["user_1"]["websocket"]
                if websocket is not None:
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": False})
        else:
            if self.chats[chat_id]["user_1"]["user_id"] == user_id:
                self.chats[chat_id]["user_1"]["user_id"] = None
                self.chats[chat_id]["user_1"]["websocket"] = None

                websocket = self.chats[chat_id]["user_2"]["websocket"]
                if websocket is not None:
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": False})

            if self.chats[chat_id]["user_2"]["user_id"] == user_id:
                self.chats[chat_id]["user_2"]["user_id"] = None
                self.chats[chat_id]["user_2"]["websocket"] = None

                websocket = self.chats[chat_id]["user_1"]["websocket"]
                if websocket is not None:
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"online": False})

    async def send_message(self, message: dict, chat_id: int, user_id: int):
        if "user_read_messages" in message:
            if self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] == user_id:
                websocket1 = self.chats[chat_id]["chat_connections"]["user_2"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"user_read_messages": True})
            else:
                websocket1 = self.chats[chat_id]["chat_connections"]["user_1"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"user_read_messages": True})
            return

        if "user_start_typing" in message:
            if self.chats[chat_id]["user_1"]["user_id"] == user_id:
                websocket1 = self.chats[chat_id]["user_2"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"user_start_typing": True})
            else:
                websocket1 = self.chats[chat_id]["user_1"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"user_start_typing": True})
            if self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] == user_id:
                websocket2 = self.chats[chat_id]["chat_connections"]["user_2"]["websocket"]
                if websocket2 is not None:
                    if websocket2.client_state == WebSocketState.CONNECTED:
                        await websocket2.send_json({"user_start_typing": True})
            else:
                websocket2 = self.chats[chat_id]["chat_connections"]["user_1"]["websocket"]
                if websocket2 is not None:
                    if websocket2.client_state == WebSocketState.CONNECTED:
                        await websocket2.send_json({"user_start_typing": True})
            return

        if "user_stop_typing" in message:
            if self.chats[chat_id]["user_1"]["user_id"] == user_id:
                websocket1 = self.chats[chat_id]["user_2"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"user_stop_typing": True})
            else:
                websocket1 = self.chats[chat_id]["user_1"]["websocket"]
                if websocket1 is not None:
                    if websocket1.client_state == WebSocketState.CONNECTED:
                        await websocket1.send_json({"user_stop_typing": True})
            if self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] == user_id:
                websocket2 = self.chats[chat_id]["chat_connections"]["user_2"]["websocket"]
                if websocket2 is not None:
                    if websocket2.client_state == WebSocketState.CONNECTED:
                        await websocket2.send_json({"user_stop_typing": True})
            else:
                websocket2 = self.chats[chat_id]["chat_connections"]["user_1"]["websocket"]
                if websocket2 is not None:
                    if websocket2.client_state == WebSocketState.CONNECTED:
                        await websocket2.send_json({"user_stop_typing": True})
            return

        if (
            self.chats[chat_id]["user_1"]["user_id"] is None
            or self.chats[chat_id]["user_2"]["user_id"] is None
        ):
            if (
                self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] != None
                and self.chats[chat_id]["chat_connections"]["user_1"]["user_id"] != user_id
            ):
                websocket = self.chats[chat_id]["chat_connections"]["user_1"]["websocket"]
                if websocket is not None:
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"chat_id": chat_id})

            if (
                self.chats[chat_id]["chat_connections"]["user_2"]["user_id"] != None
                and self.chats[chat_id]["chat_connections"]["user_2"]["user_id"] != user_id
            ):
                websocket = self.chats[chat_id]["chat_connections"]["user_2"]["websocket"]
                if websocket is not None:
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"chat_id": chat_id})
            return
        if self.chats[chat_id]["user_1"]["user_id"] != user_id:
            websocket = self.chats[chat_id]["user_1"]["websocket"]
            if websocket is not None:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json(message)
        if self.chats[chat_id]["user_2"]["user_id"] != user_id:
            websocket = self.chats[chat_id]["user_2"]["websocket"]
            if websocket is not None:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json(message)


manager = ConnectionManager()
