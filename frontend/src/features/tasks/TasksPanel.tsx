import { useState, FormEvent } from "react";
import type { Task } from "../../types/api";

type Props = {
  tasks: Task[];
  activeTaskId: string | null;
  onCreate: (title: string) => void;
  onSelect: (task: Task) => void;
  onComplete: (task: Task) => void;
  onDelete: (task: Task) => void;
  creating: boolean;
};

export function TasksPanel({ tasks, activeTaskId, onCreate, onSelect, onComplete, onDelete, creating }: Props) {
  const [title, setTitle] = useState("");

  const submit = (e: FormEvent) => {
    e.preventDefault();
    const t = title.trim();
    if (!t) return;
    onCreate(t);
    setTitle("");
  };

  const pending = tasks.filter((t) => t.status === "active");
  const completed = tasks.filter((t) => t.status === "completed");

  return (
    <section className="card">
      <h2 className="card-title">Tasks</h2>

      <form className="task-form" onSubmit={submit}>
        <input
          type="text"
          value={title}
          placeholder="Add a task…"
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          disabled={creating}
        />
        <button type="submit" disabled={creating || !title.trim()}>
          Add
        </button>
      </form>

      {pending.length === 0 && completed.length === 0 ? (
        <div className="task-empty">No tasks yet. Add one above.</div>
      ) : null}

      {pending.length > 0 && (
        <>
          <div className="task-section-label">To do</div>
          <ul className="task-list">
            {pending.map((task) => {
              const focused = task.id === activeTaskId;
              return (
                <li
                  key={task.id}
                  className={`task-item ${focused ? "focused" : ""}`}
                  onClick={() => onSelect(task)}
                >
                  <button
                    className="task-check"
                    aria-label="Complete task"
                    onClick={(e) => {
                      e.stopPropagation();
                      onComplete(task);
                    }}
                  />
                  <span className="task-title">{task.title}</span>
                  <button
                    className="task-delete"
                    aria-label="Delete task"
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(task);
                    }}
                  >
                    ×
                  </button>
                </li>
              );
            })}
          </ul>
        </>
      )}

      {completed.length > 0 && (
        <>
          <div className="task-section-label">Completed</div>
          <ul className="task-list">
            {completed.map((task) => (
              <li key={task.id} className="task-item completed">
                <span className="task-check" aria-hidden>
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                    <path d="M2 5.5L4 7.5L8 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </span>
                <span className="task-title">{task.title}</span>
                <button
                  className="task-delete"
                  aria-label="Delete task"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(task);
                  }}
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}
