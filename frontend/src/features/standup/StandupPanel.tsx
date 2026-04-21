import { useCallback, useEffect, useMemo, useState } from "react";
import { getPrefill, saveStandup } from "../../services/standupApi";
import type { StandupEntry } from "../../types/api";
import { renderMarkdown } from "./renderMarkdown";
import { emptyForm, isFormEmpty, localDateIso, type StandupFormState } from "./standupStore";

type Props = {
  onSaved?: (entry: StandupEntry) => void;
};

export function StandupPanel({ onSaved }: Props) {
  const [form, setForm] = useState<StandupFormState>(emptyForm);
  const [prefillLoading, setPrefillLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const [copyState, setCopyState] = useState<"idle" | "copied" | "fallback">("idle");

  const today = useMemo(() => localDateIso(), []);

  useEffect(() => {
    let cancelled = false;
    setPrefillLoading(true);
    getPrefill(today)
      .then((prefill) => {
        if (cancelled) return;
        setForm((f) =>
          // only apply prefill if the user hasn't typed into Yesterday yet
          f.yesterday === "" ? { ...f, yesterday: prefill.prefill_markdown } : f
        );
      })
      .catch((e) => {
        if (!cancelled) {
          console.warn("standup prefill failed", e);
        }
      })
      .finally(() => {
        if (!cancelled) setPrefillLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [today]);

  const generated = useMemo(
    () => renderMarkdown(form.yesterday, form.today, form.blockers),
    [form]
  );

  const canGenerate = !isFormEmpty(form);
  const canSave = form.today.trim().length > 0;

  const handleCopy = useCallback(async () => {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(generated);
        setCopyState("copied");
        setTimeout(() => setCopyState("idle"), 1500);
        return;
      }
      setCopyState("fallback");
    } catch (e) {
      console.warn("clipboard write failed", e);
      setCopyState("fallback");
    }
  }, [generated]);

  const handleSave = useCallback(async () => {
    setError(null);
    setSaving(true);
    try {
      const entry = await saveStandup({
        local_date: today,
        yesterday: form.yesterday,
        today: form.today,
        blockers: form.blockers,
      });
      setSavedAt(entry.updated_at);
      onSaved?.(entry);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to save standup");
    } finally {
      setSaving(false);
    }
  }, [form, today, onSaved]);

  const fieldStyle: React.CSSProperties = {
    width: "100%",
    minHeight: 80,
    fontFamily: "inherit",
    fontSize: 14,
    padding: 8,
    boxSizing: "border-box",
  };

  return (
    <section className="standup-panel" aria-label="Standup composer">
      <h2>Standup — {today}</h2>

      {prefillLoading && <div className="muted">Loading yesterday’s completed tasks…</div>}
      {error && <div className="error-banner">{error}</div>}

      <label>
        <div>Yesterday</div>
        <textarea
          style={fieldStyle}
          value={form.yesterday}
          onChange={(e) => setForm({ ...form, yesterday: e.target.value })}
          placeholder="What you finished yesterday"
          maxLength={4000}
        />
      </label>

      <label>
        <div>Today</div>
        <textarea
          style={fieldStyle}
          value={form.today}
          onChange={(e) => setForm({ ...form, today: e.target.value })}
          placeholder="What you will focus on today"
          maxLength={4000}
        />
      </label>

      <label>
        <div>Blockers</div>
        <textarea
          style={fieldStyle}
          value={form.blockers}
          onChange={(e) => setForm({ ...form, blockers: e.target.value })}
          placeholder="Anything blocking you (optional)"
          maxLength={4000}
        />
      </label>

      <div className="standup-actions" style={{ display: "flex", gap: 8, margin: "8px 0" }}>
        <button type="button" onClick={handleCopy} disabled={!canGenerate}>
          {copyState === "copied" ? "Copied!" : "Copy Markdown"}
        </button>
        <button type="button" onClick={handleSave} disabled={!canSave || saving}>
          {saving ? "Saving…" : "Save"}
        </button>
        {savedAt && <span className="muted">Saved at {new Date(savedAt).toLocaleTimeString()}</span>}
      </div>

      <div>
        <div style={{ fontWeight: 600, marginBottom: 4 }}>Preview</div>
        <pre
          style={{
            background: "#f6f6f6",
            padding: 8,
            borderRadius: 4,
            whiteSpace: "pre-wrap",
            fontFamily: "monospace",
            fontSize: 13,
          }}
          aria-label="Standup markdown preview"
        >
          {canGenerate ? generated : "Fill at least one field to preview."}
        </pre>
        {copyState === "fallback" && (
          <div>
            <div className="muted">
              Clipboard unavailable — select the text below and copy manually:
            </div>
            <textarea
              readOnly
              style={{ ...fieldStyle, minHeight: 120 }}
              value={generated}
              onFocus={(e) => e.currentTarget.select()}
            />
          </div>
        )}
      </div>
    </section>
  );
}
