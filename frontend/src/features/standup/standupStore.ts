export type StandupFormState = {
  yesterday: string;
  today: string;
  blockers: string;
};

export const emptyForm: StandupFormState = {
  yesterday: "",
  today: "",
  blockers: "",
};

export function isFormEmpty(form: StandupFormState): boolean {
  return form.yesterday.trim() === "" && form.today.trim() === "" && form.blockers.trim() === "";
}

export function localDateIso(now: Date = new Date()): string {
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, "0");
  const d = String(now.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}
