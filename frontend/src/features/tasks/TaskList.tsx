import type { Task } from "../../types/api";

type Props = {
  tasks: Task[];
  onComplete: (id: string) => Promise<void>;
  onStartFocus: (id: string) => Promise<void>;
  onStopFocus: () => Promise<void>;
};

export function TaskList({ tasks, onComplete, onStartFocus, onStopFocus }: Props) {
  return (
    <ul>
      {tasks.map((task) => (
        <li key={task.id}>
          {task.title} ({task.status})
          <button onClick={() => onStartFocus(task.id)}>Start focus</button>
          <button onClick={() => onStopFocus()}>Stop focus</button>
          <button onClick={() => onComplete(task.id)}>Complete</button>
        </li>
      ))}
    </ul>
  );
}
