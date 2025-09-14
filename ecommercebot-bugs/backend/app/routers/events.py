
from fastapi import APIRouter, HTTPException, Depends
from backend.app.db.session import get_db
from sqlalchemy.orm import Session
from backend.app.models.artifact import Artifact
from backend.app.ws_manager import publish_event
from backend.app.utils import redis_stream_publish

router = APIRouter()

@router.post("/tasks/{task_id}/events")
def task_event(task_id: str, payload: dict, db: Session = Depends(get_db)):
    try:
        step = payload.get("step")
        artifact = payload.get("artifact")
        user_id = payload.get("user_id")
        workflow_id = payload.get("workflow_id")
        if artifact:
            filename = artifact.get("filename")
            kind = artifact.get("kind", "image")
            a = Artifact(task_id=task_id, workflow_id=workflow_id, user_id=user_id, step=step, filename=filename, kind=kind)
            db.add(a)
            db.commit()
        try:
            publish_event(task_id, payload)
        except Exception:
            pass
        try:
            redis_stream_publish(task_id, payload)
        except Exception:
            pass
        return {"status":"ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
