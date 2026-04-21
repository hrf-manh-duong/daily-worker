import { request } from "./httpClient";
import type { FocusSession } from "../types/api";

export const startFocus = (taskId: string) =>
  request<FocusSession>("/focus/start", {
    method: "POST",
    body: JSON.stringify({ task_id: taskId }),
  });

export const stopFocus = () => request<FocusSession>("/focus/stop", { method: "POST" });
