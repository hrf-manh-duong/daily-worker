export function renderMarkdown(yesterday: string, today: string, blockers: string): string {
  const y = yesterday.trim();
  const t = today.trim();
  const b = blockers.trim();
  const sections = [
    `### Yesterday\n${y.length > 0 ? y : "(none)"}`,
    `### Today\n${t}`,
    `### Blockers\n${b.length > 0 ? b : "None"}`,
  ];
  return sections.join("\n\n") + "\n";
}
