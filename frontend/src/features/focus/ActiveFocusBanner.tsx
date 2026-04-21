export function ActiveFocusBanner({ title }: { title: string | null }) {
  if (!title) return null;
  return <p>Focusing: {title}</p>;
}
