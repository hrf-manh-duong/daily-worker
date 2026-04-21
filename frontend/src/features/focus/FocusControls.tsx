export function FocusControls({
  onStop,
  hasActive,
}: {
  onStop: () => Promise<void>;
  hasActive: boolean;
}) {
  return (
    <div>
      <button disabled={!hasActive} onClick={() => onStop()}>
        Stop focus
      </button>
    </div>
  );
}
