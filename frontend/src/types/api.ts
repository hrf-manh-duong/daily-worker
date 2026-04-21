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
