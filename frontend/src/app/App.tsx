import { useCallback, useEffect, useMemo, useState } from "react";
import "./App.css";
import { FocusPanel } from "../features/focus/FocusPanel";
import { TasksPanel } from "../features/tasks/TasksPanel";
import { Timeline } from "../features/timeline/Timeline";
import { completeTask, createTask, deleteTask, listTasks } from "../services/taskApi";
import { startFocus, stopFocus } from "../services/focusApi";
import { getTodayTimeline } from "../services/timelineApi";
import type { ActivityEvent, FocusSession, Task } from "../types/api";

function deriveActiveFocus(events: ActivityEvent[]): { sessionId: string; taskId: string; startedAt: string } | null {
  const byTime = [...events].sort(
    (a, b) => new Date(b.occurred_at).getTime() - new Date(a.occurred_at).getTime()
  );
  const stopped = new Set<string>();
  for (const ev of byTime) {
    if (ev.event_type === "focus_stopped" && ev.focus_session_id) stopped.add(ev.focus_session_id);
    if (ev.event_type === "focus_started" && ev.focus_session_id && ev.task_id && !stopped.has(ev.focus_session_id)) {
      return { sessionId: ev.focus_session_id, taskId: ev.task_id, startedAt: ev.occurred_at };
    }
  }
  return null;
}

export function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const [session, setSession] = useState<FocusSession | null>(null);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const [t, ev] = await Promise.all([listTasks(), getTodayTimeline()]);
      setTasks(t);
      setEvents(ev);
      // Re-derive active session only if we don't already have one locally (server is source of truth on load)
      setSession((current) => {
        if (current) return current;
        const derived = deriveActiveFocus(ev);
        if (!derived) return null;
        return {
          id: derived.sessionId,
          task_id: derived.taskId,
          started_at: derived.startedAt,
          ended_at: null,
          state: "active",
          stop_reason: "manual",
        };
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const activeTask = useMemo(
    () => (session ? tasks.find((t) => t.id === session.task_id) ?? null : null),
    [session, tasks]
  );

  const handleCreate = async (title: string) => {
    setCreating(true);
    setError(null);
    try {
      await createTask(title);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create task");
    } finally {
      setCreating(false);
    }
  };

  const handleSelect = async (task: Task) => {
    if (task.status === "completed") return;
    if (session?.task_id === task.id) return;
    setError(null);
    try {
      if (session) await stopFocus();
      const s = await startFocus(task.id);
      setSession(s);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to start focus");
    }
  };

  const handleStop = async () => {
    if (!session) return;
    setError(null);
    try {
      await stopFocus();
      setSession(null);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to stop focus");
    }
  };

  const handleComplete = async (task: Task) => {
    setError(null);
    try {
      if (session?.task_id === task.id) {
        await stopFocus();
        setSession(null);
      }
      await completeTask(task.id);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to complete task");
    }
  };

  const handleDelete = async (task: Task) => {
    setError(null);
    try {
      await deleteTask(task.id);
      if (session?.task_id === task.id) setSession(null);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to delete task");
    }
  };

  const todayLabel = new Date().toLocaleDateString([], {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="app-shell">
      <header className="header">
        <h1>Daily Work Tracker</h1>
        <div className="date">{todayLabel}</div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <div className="layout">
        <TasksPanel
          tasks={tasks}
          activeTaskId={session?.task_id ?? null}
          onCreate={handleCreate}
          onSelect={handleSelect}
          onComplete={handleComplete}
          onDelete={handleDelete}
          creating={creating}
        />
        <FocusPanel session={session} task={activeTask} onStop={handleStop} />
        <Timeline events={events} tasks={tasks} />
      </div>
    </div>
  );
}
