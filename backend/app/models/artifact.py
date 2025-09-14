
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.app.db.base_class import Base

class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, index=True, nullable=False)
    workflow_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    step = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    kind = Column(String, nullable=False)  # image|html|thumb
    mime = Column(String, default='image/png')
    size_bytes = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
