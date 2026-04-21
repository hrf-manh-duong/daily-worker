# Phase 0 Research — Daily Standup Helper

**Feature**: 002-daily-standup-helper
**Date**: 2026-04-21

## Unknowns resolved

All Q1–Q5 clarifications from the spec are resolved. No `NEEDS CLARIFICATION`
markers remain.

| Decision | Chosen | Alternatives considered | Why this choice |
|---|---|---|---|
| Output format | Markdown only | Plain text, dual toggle | Matches where standups are typically pasted (Slack/Teams/email all render Markdown). One format avoids a UI toggle and keeps the generator a pure function. |
| Persistence | One entry per local date, overwrite on save | Ephemeral, versioned history | Overwrite matches a morning-standup ritual — the user writes once per day. Versioning adds storage and UI complexity without daily value. |
| Prefill source | Previous calendar day's completed tasks | Since last saved standup | Matches how humans think about "yesterday"; does not depend on whether a standup was saved the day before. |
| Storage runtime | In-memory (extend `MemoryStore`) | Add Postgres-backed repo now | Existing tracker runs in memory; adding DB here would be out-of-scope scope creep. Spec 001's migrations exist but runtime uses memory. |
| Markdown structure | `### Yesterday`, `### Today`, `### Blockers` H3 sections | Numbered headings, plain labels | H3 is a good middle ground — renders as a visible heading in Slack/Teams, still compact. |

## Dependency impact

- **Backend**: no new pip dependencies. Uses stdlib `datetime`, Pydantic, FastAPI,
  existing in-memory repository pattern.
- **Frontend**: no new npm dependencies. Uses built-in `navigator.clipboard` with a
  textarea + `document.execCommand("copy")` fallback gated on availability.

## Risk analysis

| ID | Risk | Likelihood | Impact | Response |
|---|---|---|---|---|
| R1 | Clipboard API unavailable (non-HTTPS, older browsers) | Low | Low | Textarea fallback with select-all on preview render. |
| R2 | Timezone drift between client and server affects "yesterday" | Low | Medium | Client sends `X-Client-Local-Date` header for prefill; server trusts it. Matches spec 001's local-timezone rule. |
| R3 | Oversized field paste (>4000 chars) | Low | Low | Server returns 422 with field error; frontend shows remaining char count. |
| R4 | Double-save race (two tabs) | Very low | Low | Single-user, single browser typical; last-write-wins on the dict key is acceptable. |
| R5 | Prefill accidentally includes tasks completed today past midnight | Low | Low | Use `completed_at.date() == yesterday_local_date` strictly; unit test covers the midnight boundary. |

## Out of scope (explicit)

- No AI/LLM rewrite of user text.
- No Slack/Teams/email auto-posting.
- No reminders/notifications.
- No multi-user, no authentication (matches spec 001 FR-011).
- No versioned history (Q3 resolution).
- No analytics / insights across historical standups.
