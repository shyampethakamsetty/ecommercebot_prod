
CREATE TABLE IF NOT EXISTS artifacts (
  id SERIAL PRIMARY KEY,
  task_id TEXT NOT NULL,
  workflow_id INTEGER,
  user_id INTEGER,
  step TEXT NOT NULL,
  filename TEXT NOT NULL,
  kind TEXT NOT NULL,
  mime TEXT DEFAULT 'image/png',
  size_bytes INTEGER,
  width INTEGER,
  height INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_artifacts_task ON artifacts(task_id);
