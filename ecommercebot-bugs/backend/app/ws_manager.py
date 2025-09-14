
# Redis-backed minimal WS manager (publish-only). For delivery, backend writes to Redis stream; worker writes to events endpoint.
import os, json, asyncio
import redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
_redis = redis.from_url(REDIS_URL)

# in-memory connections map
_connections = {}

def register_conn(task_id, ws):
    _connections.setdefault(task_id, []).append(ws)

def unregister_conn(task_id, ws):
    if task_id in _connections and ws in _connections[task_id]:
        _connections[task_id].remove(ws)

async def deliver_from_stream(task_id, ws):
    # read recent messages from stream and send them; this is simple and may duplicate
    try:
        stream = f"task_events:{task_id}"
        # read last 10 messages
        res = _redis.xrevrange(stream, count=10)
        for id, data in reversed(res):
            raw = data.get(b'data', b'{}').decode()
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {'raw': raw}
            try:
                await ws.send_json(payload)
            except Exception:
                pass
    except Exception:
        pass

def publish_event(task_id, payload):
    try:
        stream = f"task_events:{task_id}"
        _redis.xadd(stream, {'data': json.dumps(payload)})
    except Exception:
        pass
    # try to send to live conns
    conns = _connections.get(task_id, [])
    for ws in list(conns):
        try:
            asyncio.create_task(ws.send_json(payload))
        except Exception:
            pass
