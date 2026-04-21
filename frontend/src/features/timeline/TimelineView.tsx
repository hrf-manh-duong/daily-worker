import type { ActivityEvent } from "../../types/api";

export function TimelineView({ events }: { events: ActivityEvent[] }) {
  return (
    <ol>
      {events.map((event) => (
        <li key={event.id}>{event.event_type}</li>
      ))}
    </ol>
  );
}
