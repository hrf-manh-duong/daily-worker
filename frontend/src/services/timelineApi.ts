import { request } from "./httpClient";
import type { ActivityEvent } from "../types/api";

export const getTodayTimeline = () => request<ActivityEvent[]>("/timeline/today");
