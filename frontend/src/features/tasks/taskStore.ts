import { createTask, listTasks } from "../../services/taskApi";

export async function loadTasks() {
  return listTasks();
}

export async function addTask(title: string) {
  return createTask(title);
}
