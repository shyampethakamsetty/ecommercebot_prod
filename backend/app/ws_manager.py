
import asyncio
from typing import Dict, List

_task_queues: Dict[str, asyncio.Queue] = {}
_connections: Dict[str, List] = {}

def _get_queue(task_id: str):
    if task_id not in _task_queues:
        _task_queues[task_id] = asyncio.Queue()
    return _task_queues[task_id]

async def register_ws(task_id: str, websocket):
    if task_id not in _connections:
        _connections[task_id] = []
    _connections[task_id].append(websocket)
    queue = _get_queue(task_id)
    while not queue.empty():
        ev = await queue.get()
        try:
            await websocket.send_json(ev)
        except Exception:
            pass

async def unregister_ws(task_id: str, websocket):
    if task_id in _connections and websocket in _connections[task_id]:
        _connections[task_id].remove(websocket)

def ws_broadcast_event(task_id: str, payload: dict):
    queue = _get_queue(task_id)
    try:
        queue.put_nowait(payload)
    except Exception:
        pass
    conns = _connections.get(task_id, [])
    for ws in list(conns):
        try:
            asyncio.create_task(ws.send_json(payload))
        except Exception:
            pass
