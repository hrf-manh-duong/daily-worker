# Implementation Plan: Daily Standup Helper

**Branch**: `002-daily-standup-helper` | **Date**: 2026-04-21 | **Spec**: `/specs/002-daily-standup-helper/spec.md`
**Input**: Feature specification from `/specs/002-daily-standup-helper/spec.md`

## Summary

Add a single-user standup composer on top of the existing Daily Work Tracker. The user
opens a form, reviews a yesterday-prefill derived from tasks they completed the previous
local day, fills "today" and "blockers", and generates a Markdown summary they can copy
to the clipboard. The entry is persisted one-per-local-date with overwrite semantics,
and a history view lists past entries newest-first. All business logic lives in a new
`standup_service`; the controller layer only parses requests and returns responses.
The feature runs on the same in-memory runtime as spec 001 (no RDBMS change), and
reuses the task query via a narrow port exposed by `task_service`.

## Technical Context

**Language/Version**: Python 3.12 (backend), Node.js 20 + TypeScript 5.6 (frontend)
**Primary Dependencies**: FastAPI, Pydantic (backend); React 18, Vite 5 (frontend)
**Storage**: In-memory (`MemoryStore.standup_entries`), keyed by local `date` for
uniqueness. No RDBMS migration added in this release (see spec AV-006).
**Testing**: pytest for backend (unit + contract); Vitest + React Testing Library for
frontend; manual smoke via local dev server for the copy flow.
**Target Platform**: Local Linux desktop dev environment (HTTPS/localhost for clipboard
API availability).
**Project Type**: Web application — thin React feature module + FastAPI routes +
service/repository pair following spec 001's layering.
**Performance Goals**: p95 API latency <150ms locally for all three endpoints (prefill,
save, list). Markdown generation is O(n) over input length; target <5ms client-side.
**Constraints**: Single-user, no notifications, no AI rewrite, no Slack auto-post.
Must not mutate tracker data. Must follow service-layer / thin-controller constitution.
**Scale/Scope**: One active user, ≤1 standup/day, history bounded by days-of-use
(hundreds of entries max).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Service-layer ownership is explicit for each business capability (no business logic in controllers).
- [x] Controller responsibilities are limited to transport concerns and service delegation.
- [x] Reuse scan completed and documented for existing modules/utilities before adding new code.
- [x] Validation strategy is defined for all external inputs and critical invariants.
- [x] Module boundaries and allowed inter-module dependencies are documented.
- [x] If schema changes are proposed, explicit approval evidence is linked; otherwise confirm no schema change.
  - Confirmed: no RDBMS schema change; in-memory store extended (see spec AV-006).

## Project Structure

### Documentation (this feature)

```text
specs/002-daily-standup-helper/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI fragment)
└── tasks.md             # Phase 2 output (written at /tasks step)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   └── standup.py            # NEW — thin controller
│   │   └── schemas/
│   │       └── standup_schema.py     # NEW — Pydantic request/response
│   ├── services/
│   │   ├── core.py                   # extended: add StandupService
│   │   └── standup_service.py        # NEW — re-export (match task_service.py pattern)
│   ├── repositories/
│   │   └── memory.py                 # extended: StandupRepository + dict on MemoryStore
│   ├── domain/
│   │   └── models.py                 # extended: StandupEntry dataclass
│   └── api/
│       └── dependencies.py           # extended: wire StandupService
└── tests/
    ├── unit/                         # service unit tests
    ├── integration/                  # route integration tests
    └── contract/                     # OpenAPI contract check

frontend/
├── src/
│   ├── features/
│   │   └── standup/                  # NEW feature module
│   │       ├── StandupPanel.tsx      # composer + preview + copy
│   │       ├── StandupHistory.tsx    # past entries list/detail
│   │       ├── standupStore.ts       # local state (form + last generated md)
│   │       └── renderMarkdown.ts     # pure fn: fields → Markdown string
│   ├── services/
│   │   └── standupApi.ts             # NEW — fetch wrappers
│   └── types/
│       └── api.ts                    # extended: StandupEntry, StandupPrefill
```

**Structure Decision**: Mirror spec 001's split. One new backend route file, one new
service class, one new repository extension, one new dataclass. One new frontend
feature folder. Reuse `MemoryStore`, `task_service.list_tasks`, and the existing
`httpClient.ts` without modification.

## Reuse Analysis

| Existing module | Reuse in this feature | Why not duplicate |
|---|---|---|
| `TaskService.list_tasks()` | Yesterday-prefill queries this and filters by `completed_at` falling on the previous local day. | Task filtering by completion date is a read-only projection; no new repository method is needed if we filter in the service. If a dedicated query is later justified by perf, add `list_completed_on(local_date)` on `TaskRepository` behind an interface. |
| `MemoryStore` | Add one dict `standup_entries: dict[date, StandupEntry]`. | Keeps single source-of-truth in-memory state; avoids a parallel store. |
| `httpClient.ts` (frontend) | Call `/api/standup/*` endpoints through the shared fetch wrapper. | Avoids a new HTTP layer and keeps error handling consistent. |
| `domain.models` | Add `StandupEntry` dataclass alongside `Task`/`FocusSession`/`ActivityEvent`. | Same dataclass style, same `_now`/`date` helpers. |
| Activity event log | NOT extended. Standup entries are distinct from activity events and must not pollute the timeline (spec SC-004). | Activity timeline is a tracker-owned concept; coupling would violate module boundaries. |

## Module Boundaries

- `standup_service` MAY depend on `task_service` (read-only, via its public `list_tasks`).
- `standup_service` MUST NOT depend on `focus_service`, `timeline_service`, or any
  repository other than `StandupRepository`.
- `StandupRepository` owns all access to `MemoryStore.standup_entries`.
- Routes in `api/routes/standup.py` MUST only parse Pydantic input, call
  `StandupService`, and map results to response schemas.
- Frontend `features/standup` MUST not import from `features/tasks` internals; it may
  consume the same API surface via its own `standupApi.ts`.

## Validation Strategy

- **Input (backend)**:
  - `yesterday`, `today`, `blockers`: each a string, max 4000 chars after trim. Empty
    allowed for `blockers` and (after prefill edit) `yesterday`. `today` MUST be
    non-empty when saving.
  - `local_date` (save/list endpoints): ISO `YYYY-MM-DD`. If omitted on save, server
    uses the user's local date as sent in `X-Client-Local-Date` header; absent header
    falls back to server UTC date (acceptable given single-user, local deployment).
  - Trim leading/trailing whitespace on all three text fields before storing.
- **Invariants**:
  - At most one `StandupEntry` per `local_date` (enforced by dict key).
  - Saving the same date overwrites atomically (single dict assignment).
  - Generating the Markdown is a pure function of the three trimmed fields; never
    raises.
- **Output**:
  - History list endpoint returns entries sorted by `local_date` descending, with a
    hard cap of 365 entries per response (single-user scale).

## Phase 0 Research Output

- Research document: `/specs/002-daily-standup-helper/research.md`
- Open questions resolved in spec §Clarifications (Q1–Q5). No `NEEDS CLARIFICATION`
  markers remain.
- Risks:
  - R1 (low): Clipboard API unavailable in non-HTTPS context — mitigation: textarea
    fallback with select-all on focus.
  - R2 (low): Timezone drift between client and server for "yesterday" — mitigation:
    client sends `X-Client-Local-Date` on prefill request; server trusts it.
  - R3 (low): Large paste into a field exceeding 4000 chars — mitigation: validation
    error with field-specific message; frontend also shows remaining char count.

## Phase 1 Design Output

- Data model: `/specs/002-daily-standup-helper/data-model.md`
- API contracts: `/specs/002-daily-standup-helper/contracts/openapi.yaml`
- Local runbook: `/specs/002-daily-standup-helper/quickstart.md`

## Post-Design Constitution Re-Check

- [x] Service-layer ownership remains explicit (`StandupService` in `services/core.py`,
  re-exported from `services/standup_service.py`).
- [x] Controllers/routes remain thin (`api/routes/standup.py` only parses + delegates).
- [x] Reuse-first honored via narrow dependency on `TaskService.list_tasks` only.
- [x] Validation rules captured in data model + contract schemas + service docstrings.
- [x] Module boundaries documented above and enforced by import layout.
- [x] Schema governance: no RDBMS change; in-memory extension documented (spec AV-006).

## Complexity Tracking

No constitution violations. Complexity limited to:
- One new dataclass, one new repository class, one new service class, one new route
  file, one new frontend feature folder.
- No new third-party dependencies (clipboard API is browser-native; date math uses
  Python stdlib `datetime`).
