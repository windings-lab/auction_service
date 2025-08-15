from fastapi import WebSocket

class LotWebsocketManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, lot_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(lot_id, []).append(websocket)

    def disconnect(self, lot_id: int, websocket: WebSocket):
        if lot_id in self.active_connections:
            self.active_connections[lot_id].remove(websocket)
            if not self.active_connections[lot_id]:
                del self.active_connections[lot_id]

    async def broadcast(self, lot_id: int, message: dict):
        for connection in self.active_connections.get(lot_id, []):
            await connection.send_json(message)

manager = LotWebsocketManager()