import { useEffect, useState } from "react";
import { listStandups } from "../../services/standupApi";
import type { StandupEntry } from "../../types/api";

type Props = {
  refreshKey?: number;
};

export function StandupHistory({ refreshKey }: Props) {
  const [entries, setEntries] = useState<StandupEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    listStandups(30)
      .then((data) => {
        if (cancelled) return;
        setEntries(data);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof Error ? e.message : "Failed to load history");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  const selected = selectedDate
    ? entries.find((e) => e.local_date === selectedDate) ?? null
    : null;

  if (loading) return <div className="muted">Loading history…</div>;
  if (error) return <div className="error-banner">{error}</div>;
  if (entries.length === 0) return <div className="muted">No saved standups yet.</div>;

  return (
    <section className="standup-history" aria-label="Standup history">
      <h3>Past standups</h3>
      <div style={{ display: "flex", gap: 16 }}>
        <ul style={{ listStyle: "none", padding: 0, margin: 0, minWidth: 140 }}>
          {entries.map((e) => (
            <li key={e.local_date}>
              <button
                type="button"
                onClick={() => setSelectedDate(e.local_date)}
                style={{
                  textAlign: "left",
                  width: "100%",
                  padding: "4px 6px",
                  background: selectedDate === e.local_date ? "#e0e7ff" : "transparent",
                  border: "none",
                  cursor: "pointer",
                  borderRadius: 3,
                }}
              >
                {e.local_date}
              </button>
            </li>
          ))}
        </ul>
        <div style={{ flex: 1 }}>
          {selected ? (
            <div>
              <h4>{selected.local_date}</h4>
              <Field label="Yesterday" value={selected.yesterday} />
              <Field label="Today" value={selected.today} />
              <Field label="Blockers" value={selected.blockers || "None"} />
            </div>
          ) : (
            <div className="muted">Select a date to view the saved standup.</div>
          )}
        </div>
      </div>
    </section>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ fontWeight: 600 }}>{label}</div>
      <pre
        style={{
          margin: 0,
          padding: 6,
          background: "#fafafa",
          whiteSpace: "pre-wrap",
          fontFamily: "inherit",
          fontSize: 13,
        }}
      >
        {value || "(empty)"}
      </pre>
    </div>
  );
}
