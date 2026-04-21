import { useEffect, useState } from "react";
import type { FocusSession, Task } from "../../types/api";

type Props = {
  session: FocusSession | null;
  task: Task | null;
  onStop: () => void;
};

function formatElapsed(startedAt: string): string {
  const diff = Math.max(0, Math.floor((Date.now() - new Date(startedAt).getTime()) / 1000));
  const h = Math.floor(diff / 3600);
  const m = Math.floor((diff % 3600) / 60);
  const s = diff % 60;
  const pad = (n: number) => n.toString().padStart(2, "0");
  return h > 0 ? `${h}:${pad(m)}:${pad(s)}` : `${pad(m)}:${pad(s)}`;
}

export function FocusPanel({ session, task, onStop }: Props) {
  const [, setTick] = useState(0);

  useEffect(() => {
    if (!session) return;
    const id = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(id);
  }, [session]);

  const isActive = Boolean(session && task);

  return (
    <section className={`card focus-panel ${isActive ? "active" : ""}`}>
      {isActive ? (
        <span className="focus-status active">
          <span className="dot" />
          Focusing
        </span>
      ) : (
        <span className="focus-status">Focus</span>
      )}

      <div className="focus-timer">
        {session ? formatElapsed(session.started_at) : "00:00"}
      </div>

      {isActive && task ? (
        <div className="focus-task-title">{task.title}</div>
      ) : (
        <div className="focus-empty">Select a task to start focusing</div>
      )}

      <div className="focus-actions">
        {isActive ? (
          <button className="btn btn-danger" onClick={onStop}>
            Stop focus
          </button>
        ) : (
          <button className="btn" disabled>
            Start focus
          </button>
        )}
      </div>
    </section>
  );
}
