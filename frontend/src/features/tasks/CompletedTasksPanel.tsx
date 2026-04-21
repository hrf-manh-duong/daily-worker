import type { Task } from "../../types/api";

export function CompletedTasksPanel({ tasks }: { tasks: Task[] }) {
  const completed = tasks.filter((t) => t.status === "completed");
  return (
    <section>
      <h3>Completed work</h3>
      <ol>
        {completed.map((task) => (
          <li key={task.id}>{task.title}</li>
        ))}
      </ol>
    </section>
  );
}
