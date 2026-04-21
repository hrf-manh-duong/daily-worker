import { FormEvent, useState } from "react";

export function TaskForm({ onCreate }: { onCreate: (title: string) => Promise<void> }) {
  const [title, setTitle] = useState("");
  return (
    <form
      onSubmit={async (e: FormEvent) => {
        e.preventDefault();
        await onCreate(title);
        setTitle("");
      }}
    >
      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="New task" />
      <button type="submit">Create</button>
    </form>
  );
}
