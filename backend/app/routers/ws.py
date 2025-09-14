
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.app.ws_manager import register_ws, unregister_ws

router = APIRouter()

@router.websocket("/api/ws/tasks/{task_id}")
async def ws_tasks(websocket: WebSocket, task_id: str):
    await websocket.accept()
    await register_ws(task_id, websocket)
    try:
        while True:
            try:
                _ = await websocket.receive_text()
                await websocket.send_text("ack")
            except Exception:
                await websocket.send_text("ack")
    except WebSocketDisconnect:
        await unregister_ws(task_id, websocket)
