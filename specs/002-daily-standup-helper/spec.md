# Feature Specification: Daily Standup Helper

**Feature Branch**: `002-daily-standup-helper`
**Created**: 2026-04-21
**Status**: Draft — clarifications resolved 2026-04-21
**Input**: User description: "Daily Standup Helper: morning form to capture yesterday/today/blockers, generate a copy-pasteable standup summary, reusing completed tasks from the existing daily work tracker"

## Clarifications

### Session 2026-04-21

- Q1: Output format for generated standup? → **A: Markdown only** (single deterministic format, no user toggle).
- Q2: Persist standups vs ephemeral? → **A: Persist** each day's standup for later review.
- Q3: Saves per calendar day? → **A: Exactly one per local date**; saving again overwrites the existing entry for that date.
- Q4: "Yesterday" prefill source? → **A: Tasks completed on the previous calendar day** in the user's local timezone, from the existing tracker.
- Q5: Blockers field required to generate? → **A: Optional**; when empty the generated summary renders "Blockers: None".

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Compose and Copy Today's Standup (Priority: P1)

As the single user, I open the standup helper in the morning, fill in what I did yesterday,
what I plan to do today, and any blockers, then copy a formatted summary to paste into a
Slack/Teams message.

**Why this priority**: This is the minimum needed to save the user time versus hand-writing
a standup message every morning. Without it, the feature has no value.

**Independent Test**: Open the standup form, fill all three fields, click "Generate",
verify a formatted summary appears, click "Copy", and verify the clipboard contains the
formatted text.

**Acceptance Scenarios**:

1. **Given** the standup form is open and empty, **When** the user types content into
   yesterday, today, and blockers fields and clicks "Generate", **Then** a formatted
   summary is displayed containing all three sections.
2. **Given** a generated summary is displayed, **When** the user clicks "Copy", **Then**
   the clipboard contains the summary text and a confirmation is shown.
3. **Given** the yesterday and today fields are filled but blockers is empty, **When**
   the user generates the summary, **Then** the summary renders a "Blockers: None" line
   (or equivalent) rather than omitting the section silently.

---

### User Story 2 - Auto-Prefill Yesterday From Completed Tasks (Priority: P2)

As the single user, when I open the standup helper, the "yesterday" field is pre-populated
with a bullet list of the tasks I completed on the previous calendar day, so I do not
have to re-type what I already logged in the work tracker.

**Why this priority**: This is where the standup helper becomes distinctly better than a
blank text box. It reuses data already captured by the existing daily-work-tracker
feature and removes duplicate data entry.

**Independent Test**: Complete 2–3 tasks on day N using the existing tracker. On day N+1,
open the standup helper. Verify the yesterday field is pre-filled with bullets matching
those completed task titles, in completion order.

**Acceptance Scenarios**:

1. **Given** the user completed tasks T1 and T2 on the previous calendar day, **When**
   the user opens the standup helper today, **Then** the yesterday field contains
   "- T1" and "- T2" in completion order as an editable prefill.
2. **Given** no tasks were completed on the previous calendar day, **When** the user
   opens the standup helper, **Then** the yesterday field is empty (no error, no
   placeholder bullets).
3. **Given** the yesterday field is prefilled, **When** the user edits or deletes the
   prefill text before generating, **Then** the generated summary reflects the user's
   edits, not the original prefill.

---

### User Story 3 - Review Past Standups (Priority: P3)

As the single user, I can open a list of past standups and view what I wrote each day,
so I can recall prior commitments and recurring blockers.

**Why this priority**: Useful for weekly reviews and retrospective context, but not
required to deliver immediate daily value.

**Independent Test**: Generate and save standups on three separate days, open the history
view, and verify the three entries are listed in reverse chronological order with their
contents visible.

**Acceptance Scenarios**:

1. **Given** saved standups exist for multiple days, **When** the user opens history,
   **Then** entries are listed newest-first with the date visible.
2. **Given** a saved standup is selected, **When** the user opens it, **Then** the
   yesterday/today/blockers fields are shown as saved.

---

### Edge Cases

- User opens the helper but all three fields stay empty — "Generate" should be disabled
  or produce an informative empty-state message rather than an empty summary.
- User generates a summary, edits a field, then clicks "Copy" without re-generating — the
  clipboard MUST contain the most recent generated text, not the stale text (resolve by
  regenerating on copy or disabling copy after edits).
- Previous day had an active focus session auto-stopped at 23:59:59 — the prefill uses
  completed tasks only, so auto-stopped focus sessions without task completion do not
  pollute the yesterday field.
- User's local timezone is used to define "yesterday" (matches existing tracker
  convention per constitution and spec 001).
- Clipboard API unavailable (e.g., non-HTTPS context) — fall back to a text area the user
  can manually select and copy.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a form with three fields: yesterday, today, blockers.
- **FR-002**: System MUST allow the user to generate a formatted standup summary from the
  three fields on demand.
- **FR-003**: System MUST provide a one-click copy action that places the generated
  summary on the system clipboard.
- **FR-004**: System MUST prefill the yesterday field with titles of tasks completed on
  the previous calendar day (user's local timezone), sourced from the existing
  daily-work-tracker task records.
- **FR-005**: System MUST allow the user to edit the prefilled yesterday content before
  generating; generated output MUST reflect the edited content.
- **FR-006**: System MUST handle the no-completed-tasks case by leaving yesterday empty
  without error.
- **FR-007**: System MUST render the blockers section in the generated summary even when
  the user entered no blockers, using the literal text "Blockers: None" (Q5 resolved:
  optional field, generation never blocked on empty blockers).
- **FR-008**: System MUST produce the summary in Markdown format (Q1 resolved) with
  three H3 headings — `### Yesterday`, `### Today`, `### Blockers` — each followed by
  the corresponding field content preserved verbatim; bullet lists in the source fields
  remain bullets.
- **FR-009**: System MUST treat "yesterday" as the previous calendar day in the user's
  local timezone, consistent with spec 001's timezone rule (FR-015 of 001).
- **FR-010**: System MUST NOT modify or delete any existing tracker data when generating
  or saving a standup.
- **FR-011**: System MUST operate for the single user only; no collaboration features.
- **FR-012**: System MUST persist each saved standup with its local date and the three
  field contents, and provide a list-and-detail history view (Q2 resolved: persist).
- **FR-013**: System MUST allow at most one standup entry per local calendar date;
  saving a standup for a date that already has an entry MUST overwrite that entry
  atomically (Q3 resolved: one-per-day, overwrite semantics).
- **FR-014**: System MUST expose a history endpoint returning saved standup entries
  ordered by local date, newest first.

### Architecture & Validation Constraints *(mandatory)*

- **AV-001**: All business logic for this feature MUST reside in service-layer modules
  (e.g., `standup_service`), consistent with the constitution.
- **AV-002**: Controllers/routes MUST only parse requests, call services, and map
  responses.
- **AV-003**: Reuse analysis MUST evaluate existing `task_service` for the yesterday
  prefill (completed-tasks query) and document why any new query cannot reuse it.
- **AV-004**: Input validation rules MUST be explicitly defined: max field lengths,
  allowed characters, UTF-8 handling, and stripping of leading/trailing whitespace.
- **AV-005**: Module boundaries — the standup module MAY depend on the task query
  interface exposed by `task_service`, but MUST NOT reach into task repositories or
  domain internals directly.
- **AV-006**: No RDBMS schema change in this release. The existing tracker runtime uses
  an in-memory store (`repositories.memory.MemoryStore`), and this feature MUST follow
  the same pattern by adding a `standup_entries` collection to that store. If DB-backed
  persistence is later adopted for the whole project, a separate migration
  `0002_standup.sql` (one table `standup_entry` with a unique constraint on local date)
  will be introduced under the constitution's schema-approval rule. Rollback for the
  in-memory change is removal of the `standup_entries` collection and related
  repository/service code; zero impact on existing modules.

### Key Entities *(include if feature involves data)*

- **Standup Entry**: A record for one local calendar date containing the yesterday,
  today, and blockers text. Uniqueness is enforced on the local date: at most one
  entry exists per date, and re-saving overwrites.
- **Generated Summary** *(transient)*: A deterministic formatted text derived from the
  three fields; not persisted on its own — the source fields are the canonical data.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The user can produce a ready-to-paste standup in under 30 seconds on a day
  where yesterday was prefilled from completed tasks.
- **SC-002**: 100% of copy actions place the exact visible generated summary on the
  clipboard (no trailing whitespace divergence, no missing sections).
- **SC-003**: 100% of standup openings on a day following a day with ≥1 completed task
  show that task in the yesterday prefill.
- **SC-004**: 0 writes are made to task/focus/timeline data as a side effect of opening,
  generating, or copying a standup.

## Assumptions

- Primary and only user is one individual, matching spec 001's single-user model.
- Desktop browser is the default context; clipboard API is available in typical
  deployment (HTTPS or localhost).
- The existing `task_service` exposes or can be extended to expose a query for tasks
  completed within a local-day window without coupling to internal repository details.
- "Yesterday" always means the previous calendar day in the user's local timezone at
  the moment the standup is opened; no weekend/Monday-rollback logic in this release.
- AI-generated rewrites/summaries are explicitly out of scope for this release (same
  exclusion stance as spec 001 FR-012).
- Multi-user, notifications, and external posting (auto-send to Slack) are out of
  scope.
