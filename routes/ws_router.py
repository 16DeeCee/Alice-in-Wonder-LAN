from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from scripts.websockets import WebSocketConnection

ws_manager = WebSocketConnection()
router = APIRouter()

@router.websocket("/chat")
async def websocket_router(websocket: WebSocket):
    validated_user = await ws_manager.ws_connect(websocket)

    if not validated_user:
        return
    
    try:
        while True:
            data = await websocket.receive_json()

            await ws_manager.broadcast(validated_user, data)
    except WebSocketDisconnect:
        ws_manager.ws_disconnect(validated_user)
