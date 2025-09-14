
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from backend.app.db.session import get_db
from backend.app.models.artifact import Artifact

router = APIRouter()
ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "/tmp/worker-data")

@router.get("/tasks/{task_id}/artifacts")
def list_artifacts(task_id: str, db: Session = Depends(get_db)):
    rows = db.query(Artifact).filter(Artifact.task_id == task_id).all()
    res = []
    for a in rows:
        res.append({
            "filename": a.filename,
            "url": f"/api/artifacts/{a.filename}",
            "step": a.step,
            "kind": a.kind,
            "mime": a.mime,
            "size_bytes": a.size_bytes,
            "created_at": a.created_at.isoformat() if a.created_at else None
        })
    return {"task_id": task_id, "artifacts": res}

@router.get("/artifacts/{filename}")
def serve_artifact(filename: str):
    fp = os.path.join(ARTIFACTS_DIR, filename)
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="Not found")
    from fastapi.responses import FileResponse
    return FileResponse(fp)
