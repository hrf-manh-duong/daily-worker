# Data Model — Daily Standup Helper

**Feature**: 002-daily-standup-helper
**Date**: 2026-04-21

## Entities

### StandupEntry

Represents a saved standup for one local calendar date.

| Field | Type | Required | Notes |
|---|---|---|---|
| `local_date` | `date` | yes | Primary key (unique per local date). Source of truth for "which day". |
| `yesterday` | `str` | yes (may be empty string) | Free-text Markdown-friendly content. Max 4000 chars (trimmed). |
| `today` | `str` | yes, non-empty | Max 4000 chars (trimmed). |
| `blockers` | `str` | yes (may be empty string) | Max 4000 chars (trimmed). Empty renders as "None" in generated summary. |
| `created_at` | `datetime` | yes | First-save UTC timestamp. |
| `updated_at` | `datetime` | yes | Most-recent-save UTC timestamp. Equals `created_at` on first save. |

**Invariants**:

- `local_date` is unique across all `StandupEntry` instances.
- `yesterday`, `today`, `blockers` are stored with leading/trailing whitespace stripped.
- Overwrite semantics: saving for an existing `local_date` preserves `created_at` and
  updates `updated_at`, `yesterday`, `today`, `blockers`.
- Never references or mutates `Task`, `FocusSession`, or `ActivityEvent`.

### StandupPrefill (transient, not persisted)

Result of the yesterday-prefill query.

| Field | Type | Notes |
|---|---|---|
| `for_local_date` | `date` | Today's local date the prefill is intended for. |
| `source_local_date` | `date` | Equal to `for_local_date - 1 day`. |
| `completed_tasks` | `list[str]` | Task titles completed on `source_local_date`, in ascending `completed_at` order. |
| `prefill_markdown` | `str` | `"- {title}"` lines joined by `\n`; empty string if no completed tasks. |

### Generated Summary (transient, never persisted)

Pure function `render_markdown(yesterday, today, blockers) -> str`:

```
### Yesterday
{yesterday or "(none)"}

### Today
{today}

### Blockers
{blockers or "None"}
```

Rules:

- Each section's body is the trimmed field verbatim.
- The entire output ends with a single trailing `\n`.
- Function is deterministic; unit-testable in isolation.

## Storage layout (in-memory)

Extension to `repositories.memory.MemoryStore`:

```python
standup_entries: dict[date, StandupEntry] = {}
```

All access goes through a new `StandupRepository` (to preserve the pattern used by
`TaskRepository`, `FocusRepository`, `ActivityRepository`).

## Validation rules summary

| Rule | Enforced at |
|---|---|
| `today` non-empty after trim | Service (`StandupService.save`) |
| Each field ≤ 4000 chars after trim | Pydantic schema + service guard |
| `local_date` parseable as ISO date | Pydantic schema |
| At most one entry per `local_date` | Repository (dict key uniqueness) |
| Read-only access to tasks | Service depends only on `TaskService.list_tasks`, not on `TaskRepository` directly |
