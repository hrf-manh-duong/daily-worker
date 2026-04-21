import { getTodayTimeline } from "../../services/timelineApi";

export async function loadTodayTimeline() {
  return getTodayTimeline();
}
