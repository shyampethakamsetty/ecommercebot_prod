
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.app.ws_manager import register_conn, unregister_conn, deliver_from_stream
import os
router = APIRouter()

@router.websocket("/api/ws/tasks/{task_id}")
async def ws_tasks(websocket: WebSocket, task_id: str):
    # Auth: token query param or header must match WS_AUTH_TOKEN if set
    params = websocket.query_params
    token = params.get('token') or websocket.headers.get('sec-websocket-protocol')
    expected = os.getenv('WS_AUTH_TOKEN')
    if expected and token != expected:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    register_conn(task_id, websocket)
    # send recent stream entries
    try:
        await deliver_from_stream(task_id, websocket)
    except Exception:
        pass
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        unregister_conn(task_id, websocket)
