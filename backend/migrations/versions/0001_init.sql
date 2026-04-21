CREATE TABLE IF NOT EXISTS tasks (
  id UUID PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  status VARCHAR(16) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS focus_sessions (
  id UUID PRIMARY KEY,
  task_id UUID NOT NULL REFERENCES tasks(id),
  started_at TIMESTAMPTZ NOT NULL,
  ended_at TIMESTAMPTZ NULL,
  state VARCHAR(16) NOT NULL,
  stop_reason VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS activity_events (
  id UUID PRIMARY KEY,
  event_type VARCHAR(32) NOT NULL,
  task_id UUID NULL REFERENCES tasks(id),
  focus_session_id UUID NULL REFERENCES focus_sessions(id),
  occurred_at TIMESTAMPTZ NOT NULL,
  local_day DATE NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb
);
