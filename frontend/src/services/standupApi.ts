import { request } from "./httpClient";
import type { StandupEntry, StandupPrefill, StandupSavePayload } from "../types/api";

export const getPrefill = (localDate: string) =>
  request<StandupPrefill>("/standup/prefill", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Client-Local-Date": localDate,
    },
  });

export const saveStandup = (payload: StandupSavePayload) =>
  request<StandupEntry>("/standup", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const listStandups = (limit = 30) =>
  request<StandupEntry[]>(`/standup?limit=${limit}`);

export const getStandup = (localDate: string) =>
  request<StandupEntry>(`/standup/${localDate}`);
