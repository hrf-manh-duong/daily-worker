import { startFocus, stopFocus } from "../../services/focusApi";

export async function beginFocus(taskId: string) {
  return startFocus(taskId);
}

export async function endFocus() {
  return stopFocus();
}
