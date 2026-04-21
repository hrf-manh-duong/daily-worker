---

description: "Task list for Daily Standup Helper implementation"
---

# Tasks: Daily Standup Helper

**Input**: Design documents from `/specs/002-daily-standup-helper/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

**Tests**: Contract, integration, and unit tests are included — the constitution requires explicit validation coverage for every feature path, and the existing Daily Work Tracker (spec 001) already establishes the test layout under `backend/tests/` and `frontend/tests/`.

**Organization**: Tasks are grouped by user story so each story is independently implementable and testable. Setup is a thin "extension" phase because the project scaffolding from feature 001 is already in place.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependency)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`)
- Every task includes objective, likely files, validation, testing, and logging/monitoring notes where relevant.

---

## Phase 1: Foundational Extension (Blocking Prerequisites)

**Purpose**: Extend the existing in-memory store, domain model, DTOs, service skeleton, route skeleton, DI wiring, and frontend API client in line with spec 001's patterns. No new dependencies. No RDBMS schema change (see spec AV-006).

- [ ] T001 Objective: add `StandupEntry` dataclass to the domain model | Files: `backend/src/domain/models.py`, `backend/src/domain/standup.py` (new re-export to mirror `task.py` pattern) | Validation: fields and invariants match `data-model.md` (local_date PK, 4000-char fields, created_at/updated_at) | Testing: add unit test `backend/tests/unit/test_domain_models.py::test_standup_entry_*` covering trim + defaults | Logging: N/A (pure data class)
- [ ] T002 Objective: extend `MemoryStore` with `standup_entries: dict[date, StandupEntry]` and add `StandupRepository` | Files: `backend/src/repositories/memory.py`, `backend/src/repositories/standup_repository.py` (new re-export) | Validation: repository exposes `upsert(entry)`, `get(local_date)`, `list(limit)` and enforces one-entry-per-date via dict key | Testing: `backend/tests/integration/test_repositories.py::test_standup_repository_*` — upsert overwrites, list is newest-first | Logging: N/A
- [ ] T003 [P] Objective: add Pydantic request/response schemas | Files: `backend/src/api/schemas/standup_schema.py` | Validation: mirrors `contracts/openapi.yaml` (StandupSaveRequest, StandupEntry, StandupPrefill); max 4000 chars per text field; `today` min 1 after trim | Testing: `backend/tests/unit/test_api_schemas.py::test_standup_*` — valid payload, oversized field rejected, empty `today` rejected | Logging: N/A
- [ ] T004 Objective: add `StandupService` skeleton in `services/core.py` and re-export from `services/standup_service.py` | Files: `backend/src/services/core.py`, `backend/src/services/standup_service.py` (new) | Validation: class constructor takes `StandupRepository` + `TaskService` (read-only dep); methods `get_prefill(for_local_date)`, `save(local_date, yesterday, today, blockers)`, `get(local_date)`, `list(limit)` stubbed with correct signatures | Testing: N/A (skeleton; real tests land in per-story phases) | Logging: service entry/debug logs pattern matches `task_service`
- [ ] T005 [P] Objective: create thin route module for `/api/standup` | Files: `backend/src/api/routes/standup.py` | Validation: only parses Pydantic input, calls service, maps response — no conditional business logic | Testing: `backend/tests/unit/test_route_service_boundary.py` asserts no business branching in the new routes module | Logging: request/response summary logs
- [ ] T006 Objective: wire new service and repository into DI + register router | Files: `backend/src/api/dependencies.py`, `backend/src/main.py` | Validation: `GET /api/standup` returns `[]` after boot; FastAPI app health check still passes | Testing: extend `backend/tests/integration/test_app_boot.py` to assert the standup router is mounted | Logging: DI construction logs remain at debug level
- [ ] T007 [P] Objective: add frontend API client and types for standup endpoints | Files: `frontend/src/services/standupApi.ts` (new), `frontend/src/types/api.ts` (extend) | Validation: methods `getPrefill(localDate)`, `saveStandup(payload)`, `listStandups(limit)`, `getStandup(localDate)` — all wired through the shared `httpClient` | Testing: `frontend/tests/services/apiClients.test.ts` extended with standup endpoint mappings | Logging: client error logging via `httpClient` interceptor

**Checkpoint**: Foundational extension complete; all three user stories can proceed independently.

---

## Phase 2: User Story 1 - Compose and Copy Today's Standup (Priority: P1) 🎯 MVP

**Goal**: Let the user fill Yesterday/Today/Blockers, click Generate to render a Markdown summary, and Copy it to the clipboard.

**Independent Test**: Open the Standup panel, type content into all three fields, click Generate, verify Markdown preview renders; click Copy, verify clipboard contains the same text.

### Tests for User Story 1

- [ ] T008 [P] [US1] Objective: add pure-function unit tests for Markdown renderer | Files: `backend/tests/unit/test_standup_service.py` (or a dedicated `test_render_markdown.py` if renderer lives in its own module) | Validation: three H3 sections, `Blockers: None` when empty, trimmed fields verbatim, deterministic output, trailing newline | Testing: parametrized cases covering all-filled, empty blockers, multi-line input | Logging: N/A
- [ ] T009 [P] [US1] Objective: add contract test for `POST /api/standup` happy path | Files: `backend/tests/contract/test_standup_contract.py` (new) | Validation: 200 response matches `StandupEntry` schema from `contracts/openapi.yaml`; 422 when `today` empty or field > 4000 chars | Testing: include `local_date` echo in response | Logging: N/A
- [ ] T010 [P] [US1] Objective: add frontend component tests for StandupPanel compose/generate/copy | Files: `frontend/tests/features/standup/StandupPanel.test.tsx` (new) | Validation: Generate button disabled when all three fields empty; clicking Copy writes expected text to the `navigator.clipboard` mock; textarea fallback triggers when clipboard mock throws | Testing: Testing Library with userEvent | Logging: N/A

### Implementation for User Story 1

- [ ] T011 [US1] Objective: implement pure Markdown renderer on the backend (and mirror on the frontend for instant preview without a round-trip) | Files: `backend/src/services/core.py` (helper `_render_markdown` used by `save` for an optional `generated` response field — OR — keep rendering entirely client-side; choose one path and document it), `frontend/src/features/standup/renderMarkdown.ts` (new, client-side, pure) | Validation: matches `data-model.md` template exactly; identical output for identical inputs; handles 4000-char inputs without truncation | Testing: covered by T008 + a frontend unit test `frontend/tests/features/standup/renderMarkdown.test.ts` | Logging: N/A
- [ ] T012 [US1] Objective: implement `StandupService.save` — validates `today` non-empty, trims fields, upserts via repository, stamps `created_at`/`updated_at` | Files: `backend/src/services/core.py` | Validation: overwrite preserves `created_at`; re-save updates `updated_at` strictly >= previous; raises `ValueError("invalid_today")` on empty after trim | Testing: `backend/tests/unit/test_standup_service.py::test_save_*` | Logging: emit info log `standup_saved local_date=... overwrite=bool`
- [ ] T013 [US1] Objective: implement `POST /api/standup` and `GET /api/standup/{local_date}` route handlers (thin) | Files: `backend/src/api/routes/standup.py` | Validation: parses payload, delegates, returns mapped DTO; returns 404 when `GET /{local_date}` has no entry | Testing: `backend/tests/unit/test_standup_routes.py` (new) — invalid payload → 422, missing entry → 404, happy-path → 200 | Logging: access log with `local_date` tag
- [ ] T014 [US1] Objective: build `StandupPanel` composer — three textareas, Generate button, Markdown preview, Copy button with fallback | Files: `frontend/src/features/standup/StandupPanel.tsx` (new), `frontend/src/features/standup/standupStore.ts` (new) | Validation: regenerates preview when any field changes (or re-enables Copy only after a fresh Generate — pick the non-stale-clipboard behavior from spec Edge Cases); Copy falls back to selectable textarea if `navigator.clipboard` missing | Testing: covered by T010 | Logging: `console.warn` on copy failure only (no noisy logs)
- [ ] T015 [US1] Objective: wire StandupPanel into the app shell with a Save action that calls `POST /api/standup` | Files: `frontend/src/app/App.tsx`, `frontend/src/app/App.css` | Validation: Panel renders alongside existing Tasks/Focus/Timeline; Save shows success toast; errors surface in existing error banner | Testing: extend an existing App render test (or add `frontend/tests/app/App.standup.test.tsx`) asserting the Standup panel mounts | Logging: N/A beyond existing error-banner path

**Checkpoint**: User Story 1 is independently functional and delivers MVP value (handwritten standups work end-to-end; prefill is stubbed to empty on the backend).

---

## Phase 3: User Story 2 - Auto-Prefill Yesterday From Completed Tasks (Priority: P2)

**Goal**: On open, the Yesterday textarea is pre-filled with bullets of task titles completed on the previous local day.

**Independent Test**: Complete 2–3 tasks today, advance the local date by 1, open the Standup panel tomorrow, verify Yesterday contains `- T1` / `- T2` / `- T3` in completion order; editable.

### Tests for User Story 2

- [ ] T016 [P] [US2] Objective: add integration test for prefill across the local-day boundary | Files: `backend/tests/integration/test_standup_prefill.py` (new) | Validation: tasks completed at `yesterday 23:59` show up; tasks completed at `today 00:00` do not; active/deleted tasks excluded | Testing: freeze time around midnight boundary cases | Logging: N/A
- [ ] T017 [P] [US2] Objective: add contract test for `GET /api/standup/prefill` | Files: `backend/tests/contract/test_standup_contract.py` (extend) | Validation: response shape matches `StandupPrefill`; respects `X-Client-Local-Date` header; falls back to server UTC date when header missing | Testing: include empty-completion day (returns empty list + empty markdown) | Logging: N/A

### Implementation for User Story 2

- [ ] T018 [US2] Objective: implement `StandupService.get_prefill(for_local_date)` — queries tasks via `TaskService.list_tasks`, filters by `completed_at.date() == for_local_date - 1 day` in the user's local tz | Files: `backend/src/services/core.py` | Validation: read-only (no writes to tasks/focus/events, SC-004); excludes non-completed tasks; ascending order by `completed_at` | Testing: `backend/tests/unit/test_standup_service.py::test_get_prefill_*` including midnight boundary | Logging: debug log with `for_local_date` and result count
- [ ] T019 [US2] Objective: implement `GET /api/standup/prefill` route with `X-Client-Local-Date` header handling | Files: `backend/src/api/routes/standup.py` | Validation: header parsed to `date`; malformed header → 422; absent header → server UTC date fallback | Testing: extend `backend/tests/unit/test_standup_routes.py` | Logging: log header value (or `null`) per request
- [ ] T020 [US2] Objective: fetch prefill on mount in the frontend and hydrate the Yesterday textarea as editable initial value | Files: `frontend/src/features/standup/StandupPanel.tsx`, `frontend/src/features/standup/standupStore.ts` | Validation: user edits to the prefilled text persist; `prefill_markdown` empty leaves the textarea blank without error | Testing: `frontend/tests/features/standup/StandupPanel.prefill.test.tsx` (new) asserting mount-time fetch and edit preservation | Logging: `console.warn` on fetch failure, with fallback to empty textarea
- [ ] T021 [US2] Objective: send `X-Client-Local-Date` derived from `new Date().toLocaleDateString('en-CA')` (ISO YYYY-MM-DD in local tz) on the prefill request | Files: `frontend/src/services/standupApi.ts` | Validation: header is set on the prefill call only; other calls unchanged | Testing: extend `frontend/tests/services/apiClients.test.ts` to assert the header is attached | Logging: N/A

**Checkpoint**: User Stories 1 + 2 functional — the user opens the panel and gets a sensible starting point every day.

---

## Phase 4: User Story 3 - Review Past Standups (Priority: P3)

**Goal**: A history list shows saved standups newest-first; selecting one reveals the yesterday/today/blockers as saved.

**Independent Test**: Save three standups on three distinct dates (or by setting `local_date` directly in the save payload). Open history, verify reverse-chronological list; click one, verify detail view matches what was saved.

### Tests for User Story 3

- [ ] T022 [P] [US3] Objective: add contract test for `GET /api/standup` list and the `limit` query param | Files: `backend/tests/contract/test_standup_contract.py` (extend) | Validation: default `limit=30`, max `365`; ordering `local_date DESC`; payload items match `StandupEntry` schema | Testing: include empty-history case | Logging: N/A
- [ ] T023 [P] [US3] Objective: add frontend component tests for `StandupHistory` | Files: `frontend/tests/features/standup/StandupHistory.test.tsx` (new) | Validation: entries rendered in received order (assume server already sorts); clicking an entry reveals fields in read-only form | Testing: Testing Library | Logging: N/A

### Implementation for User Story 3

- [ ] T024 [US3] Objective: implement `StandupService.list(limit)` — returns entries sorted by `local_date DESC` capped at min(limit, 365) | Files: `backend/src/services/core.py` | Validation: stable order, cap enforced, no side effects | Testing: `backend/tests/unit/test_standup_service.py::test_list_*` | Logging: debug log with returned count
- [ ] T025 [US3] Objective: implement `GET /api/standup` route with `limit` query param | Files: `backend/src/api/routes/standup.py` | Validation: delegate-only, query validation via Pydantic `Query(ge=1, le=365)` | Testing: extend `backend/tests/unit/test_standup_routes.py` | Logging: log returned count
- [ ] T026 [US3] Objective: build `StandupHistory` UI with list + detail view (inline expand or side-by-side) | Files: `frontend/src/features/standup/StandupHistory.tsx` (new) | Validation: list renders newest-first; selecting an entry shows the saved fields in a read-only view; loading/empty states handled | Testing: covered by T023 | Logging: N/A
- [ ] T027 [US3] Objective: expose history from the main app shell (tab/toggle next to the composer) | Files: `frontend/src/app/App.tsx` | Validation: switching between Compose and History does not lose unsaved composer state | Testing: extend app-level render test to assert both views reachable | Logging: N/A

**Checkpoint**: All three user stories functional; end-to-end daily ritual is covered.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, manual smoke pass, and constitution-check close-out.

- [ ] T028 [P] Objective: run full backend + frontend test suites and fix any regressions | Files: `backend/tests/`, `frontend/tests/` | Validation: `pytest -q` green; `npm run test` green | Testing: execute both suites | Logging: capture test output if any failures
- [ ] T029 Objective: execute the Quickstart manual test (happy path + edge cases) | Files: `specs/002-daily-standup-helper/quickstart.md` | Validation: every step reproducible in a fresh dev run; clipboard flow works in Chrome + Firefox on localhost | Testing: manual | Logging: verify no writes to tasks/focus/events during standup operations (SC-004)
- [ ] T030 Objective: close the constitution gate — service-layer ownership, thin controllers, reuse of `TaskService.list_tasks`, validation coverage, module-boundary imports, no RDBMS schema change | Files: `specs/002-daily-standup-helper/plan.md` Post-Design Re-Check | Validation: every checkbox in the post-design list is verifiable against merged code | Testing: N/A (review) | Logging: N/A
- [ ] T031 Objective: add a short "Standup Helper" section to the project-level README or local docs (optional if README does not yet exist) | Files: `README.md` (create if not yet present), linking to `specs/002-daily-standup-helper/quickstart.md` | Validation: new contributor can find the feature from the repo root | Testing: N/A | Logging: N/A

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational Extension)**: start immediately on branch `002-daily-standup-helper`.
- **Phase 2 (US1)**: depends on Phase 1; delivers MVP.
- **Phase 3 (US2)**: depends on Phase 1; strictly adds value on top of US1 but is independently demonstrable with a blank composer if US1 is partially shipped.
- **Phase 4 (US3)**: depends on Phase 1 and at least one saved entry (from US1's save path).
- **Phase 5 (Polish)**: depends on whatever user stories were selected for this release.

### Within Each User Story

- Tests before implementation where practical (contract + integration tests added first, then service, then route, then UI).
- Service implementation before route implementation.
- Backend before frontend within the same story, but frontend-only tasks marked `[P]` can start once the API contract is agreed.

### Parallel Opportunities

- Foundational `[P]`: T003, T005, T007.
- US1 tests `[P]`: T008, T009, T010.
- US2 tests `[P]`: T016, T017.
- US3 tests `[P]`: T022, T023.
- Polish `[P]`: T028.
