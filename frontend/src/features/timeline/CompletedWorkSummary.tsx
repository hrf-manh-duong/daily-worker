import type { ActivityEvent } from "../../types/api";

export function CompletedWorkSummary({ events }: { events: ActivityEvent[] }) {
  const completed = events.filter((e) => e.event_type === "task_completed");
  return (
    <section>
      <h3>Completed sequence</h3>
      <ol>
        {completed.map((event) => (
          <li key={event.id}>{event.task_id}</li>
        ))}
      </ol>
    </section>
  );
}
