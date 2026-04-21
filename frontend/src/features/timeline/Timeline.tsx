import type { ActivityEvent, Task } from "../../types/api";

type Props = {
  events: ActivityEvent[];
  tasks: Task[];
};

const EVENT_LABEL: Record<string, string> = {
  task_created: "Created",
  task_updated: "Updated",
  task_completed: "Completed",
  task_deleted: "Deleted",
  focus_started: "Started focus on",
  focus_stopped: "Stopped focus on",
};

const EVENT_KIND: Record<string, string> = {
  task_created: "created",
  task_updated: "created",
  task_completed: "completed",
  task_deleted: "stopped",
  focus_started: "started",
  focus_stopped: "stopped",
};

function formatTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: false });
}

export function Timeline({ events, tasks }: Props) {
  const taskMap = new Map(tasks.map((t) => [t.id, t]));
  const sorted = [...events].sort(
    (a, b) => new Date(b.occurred_at).getTime() - new Date(a.occurred_at).getTime()
  );

  return (
    <section className="card">
      <h2 className="card-title">Today</h2>
      {sorted.length === 0 ? (
        <div className="timeline-empty">No activity yet</div>
      ) : (
        <ul className="timeline-list">
          {sorted.map((ev) => {
            const kind = EVENT_KIND[ev.event_type] ?? "created";
            const label = EVENT_LABEL[ev.event_type] ?? ev.event_type;
            const task = ev.task_id ? taskMap.get(ev.task_id) : null;
            const payloadTitle = (ev.payload as { title?: string })?.title;
            const name = task?.title ?? payloadTitle ?? "";
            return (
              <li key={ev.id} className={`timeline-item ${kind}`}>
                <span className="timeline-dot" />
                <div className="timeline-action">
                  <span className="label">{label}</span>
                  {name ? ` ${name}` : ""}
                </div>
                <div className="timeline-time">{formatTime(ev.occurred_at)}</div>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
