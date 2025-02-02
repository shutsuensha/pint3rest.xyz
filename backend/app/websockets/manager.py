from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.chats = {}

    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int, chat_connection: bool | None = None):
        await websocket.accept()
        if chat_id not in self.chats:
            self.chats[chat_id] = {
                'user_1': {
                    'user_id': None,
                    'websocket': None
                },
                'user_2': {
                    'user_id': None,
                    'websocket': None
                },
                'chat_connections': {
                    'user_1': {
                        'user_id': None,
                        'websocket': None
                    },
                    'user_2': {
                        'user_id': None,
                        'websocket': None
                    },
                }
            }

        if chat_connection:
            if self.chats[chat_id]['chat_connections']['user_1']['user_id'] is None:
                self.chats[chat_id]['chat_connections']['user_1']['user_id'] = user_id
                self.chats[chat_id]['chat_connections']['user_1']['websocket'] = websocket
            else: 
                self.chats[chat_id]['chat_connections']['user_2']['user_id'] = user_id
                self.chats[chat_id]['chat_connections']['user_2']['websocket'] = websocket
        else:
            if self.chats[chat_id]['user_1']['user_id'] is None:
                self.chats[chat_id]['user_1']['user_id'] = user_id
                self.chats[chat_id]['user_1']['websocket'] = websocket
            else: 
                self.chats[chat_id]['user_2']['user_id'] = user_id
                self.chats[chat_id]['user_2']['websocket'] = websocket
    

    def disconnect(self, chat_id: int, user_id: int, chat_connection: bool | None = None):
        if self.chats[chat_id]['user_1']['user_id'] == user_id:
            self.chats[chat_id]['user_1']['user_id'] = None
            self.chats[chat_id]['user_1']['websocket'] = None
        
        if self.chats[chat_id]['user_2']['user_id'] == user_id:
            self.chats[chat_id]['user_2']['user_id'] = None
            self.chats[chat_id]['user_2']['websocket'] = None

        if chat_connection:
            if self.chats[chat_id]['chat_connections']['user_1']['user_id'] == user_id:
                self.chats[chat_id]['chat_connections']['user_1']['user_id'] = None
                self.chats[chat_id]['chat_connections']['user_1']['websocket'] = None
            
            if self.chats[chat_id]['chat_connections']['user_2']['user_id'] == user_id:
                self.chats[chat_id]['chat_connections']['user_2']['user_id'] = None
                self.chats[chat_id]['chat_connections']['user_2']['websocket'] = None


        if self.chats[chat_id]['chat_connections']['user_1']['user_id'] is None and self.chats[chat_id]['chat_connections']['user_2']['user_id'] is None:
            del self.chats[chat_id]


    async def send_message(self, message: dict, chat_id: int, user_id: int):
        if self.chats[chat_id]['user_1']['user_id'] is None or self.chats[chat_id]['user_2']['user_id'] is None:
            if self.chats[chat_id]['chat_connections']['user_1']['user_id'] != None and \
                self.chats[chat_id]['chat_connections']['user_1']['user_id'] != user_id:
                
                websocket = self.chats[chat_id]['chat_connections']['user_1']['websocket']
                await websocket.send_json({'chat_id': chat_id})

            if self.chats[chat_id]['chat_connections']['user_2']['user_id'] != None and \
                self.chats[chat_id]['chat_connections']['user_2']['user_id'] != user_id:
                
                websocket = self.chats[chat_id]['chat_connections']['user_2']['websocket']
                await websocket.send_json({'chat_id': chat_id})
            return
        if self.chats[chat_id]['user_1']['user_id'] != user_id:
            websocket = self.chats[chat_id]['user_1']['websocket']
            await websocket.send_json(message)
        if self.chats[chat_id]['user_2']['user_id'] != user_id:
            websocket = self.chats[chat_id]['user_2']['websocket']
            await websocket.send_json(message)



manager = ConnectionManager()