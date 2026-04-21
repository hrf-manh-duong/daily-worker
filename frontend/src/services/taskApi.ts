import { request } from "./httpClient";
import type { Task } from "../types/api";

export const listTasks = () => request<Task[]>("/tasks");
export const createTask = (title: string) =>
  request<Task>("/tasks", { method: "POST", body: JSON.stringify({ title }) });
export const updateTask = (id: string, title: string) =>
  request<Task>(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify({ title }) });
export const completeTask = (id: string) =>
  request<Task>(`/tasks/${id}/complete`, { method: "POST" });
export const deleteTask = (id: string) =>
  fetch(`${import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"}/tasks/${id}`, {
    method: "DELETE",
  }).then((r) => {
    if (!r.ok) throw new Error(`Request failed: ${r.status}`);
  });
