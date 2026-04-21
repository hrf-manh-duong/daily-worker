export type Task = {
  id: string;
  title: string;
  status: "active" | "completed";
  created_at: string;
  updated_at: string;
  completed_at: string | null;
};

export type FocusSession = {
  id: string;
  task_id: string;
  started_at: string;
  ended_at: string | null;
  state: "active" | "ended";
  stop_reason: "manual" | "day_rollover";
};

export type ActivityEvent = {
  id: string;
  event_type: string;
  task_id: string | null;
  focus_session_id: string | null;
  occurred_at: string;
  local_day: string;
  payload: Record<string, unknown>;
};

export type StandupEntry = {
  local_date: string;
  yesterday: string;
  today: string;
  blockers: string;
  created_at: string;
  updated_at: string;
};

export type StandupPrefill = {
  for_local_date: string;
  source_local_date: string;
  completed_tasks: string[];
  prefill_markdown: string;
};

export type StandupSavePayload = {
  local_date: string;
  yesterday: string;
  today: string;
  blockers: string;
};
