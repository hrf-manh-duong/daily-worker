---

description: "Task list for Daily Work Tracker MVP implementation"
---

# Tasks: Daily Work Tracker MVP

**Input**: Design documents from `/specs/001-daily-work-tracker/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

**Tests**: Include contract, integration, and unit tests because validation and correctness are core requirements.

**Organization**: Tasks are grouped by user story so each story is independently implementable and testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependency)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`)
- Every task includes objective, likely files, validation, testing, and logging/monitoring notes where relevant.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize frontend/backend workspaces and baseline tooling for local MVP.

- [X] T001 Objective: create frontend/backend folder scaffold aligned with plan | Files: `backend/src/`, `backend/tests/`, `frontend/src/`, `frontend/tests/` | Validation: directories match planned structure | Testing: N/A | Logging: N/A
- [X] T002 [P] Objective: initialize backend Python project and minimal dependencies | Files: `backend/pyproject.toml`, `backend/requirements.txt` | Validation: dependency install succeeds in clean venv | Testing: run `pytest -q` baseline | Logging: include logging package/config only if needed
- [X] T003 [P] Objective: initialize frontend React+TS app and minimal dependencies | Files: `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json` | Validation: `npm run dev` starts locally | Testing: run `npm test` baseline | Logging: browser console errors handled in dev
- [X] T004 [P] Objective: define formatting/linting and code-style enforcement rules | Files: `backend/pyproject.toml`, `frontend/eslint.config.js`, `frontend/prettier.config.cjs` | Validation: lint/format commands pass | Testing: add CI lint steps dry-run locally | Logging: N/A
- [X] T005 Objective: configure local environment templates for backend/frontend | Files: `backend/.env.example`, `frontend/.env.example` | Validation: variables match quickstart | Testing: boot app using copied `.env` files | Logging: include log-level env var in backend example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared backend architecture, persistence baseline, and cross-cutting validation/logging.

- [X] T006 Objective: set up PostgreSQL migration framework and initial schema approval note | Files: `backend/alembic.ini`, `backend/migrations/env.py`, `backend/migrations/versions/0001_init.sql`, `specs/001-daily-work-tracker/research.md` | Validation: `alembic upgrade head` succeeds | Testing: migration smoke test on empty DB | Logging: migration execution logs captured
- [X] T007 Objective: implement DB session management and repository base abstractions | Files: `backend/src/db/session.py`, `backend/src/repositories/base_repository.py` | Validation: session lifecycle works per request | Testing: unit tests with transaction rollback fixture in `backend/tests/unit/test_db_session.py` | Logging: DB connect/disconnect events at debug level
- [X] T008 Objective: add core domain models for Task, FocusSession, ActivityEvent | Files: `backend/src/domain/task.py`, `backend/src/domain/focus_session.py`, `backend/src/domain/activity_event.py` | Validation: models match data-model fields and constraints | Testing: unit model validation tests in `backend/tests/unit/test_domain_models.py` | Logging: N/A
- [X] T009 [P] Objective: implement repository classes for tasks, focus sessions, and activity events | Files: `backend/src/repositories/task_repository.py`, `backend/src/repositories/focus_repository.py`, `backend/src/repositories/activity_repository.py` | Validation: CRUD/query methods return expected records | Testing: repository integration tests in `backend/tests/integration/test_repositories.py` | Logging: query failure logs with context
- [X] T010 [P] Objective: create API schema DTOs and shared request validation rules | Files: `backend/src/api/schemas/task_schema.py`, `backend/src/api/schemas/focus_schema.py`, `backend/src/api/schemas/timeline_schema.py` | Validation: invalid payloads rejected with clear errors | Testing: schema unit tests in `backend/tests/unit/test_api_schemas.py` | Logging: validation error summaries in request logs
- [X] T011 Objective: implement shared logging/monitoring utilities for activity-centric audit trail | Files: `backend/src/logging/config.py`, `backend/src/logging/activity_logger.py` | Validation: structured logs include event type, task id, and timestamp | Testing: unit tests for logger payload shape in `backend/tests/unit/test_activity_logger.py` | Logging: core requirement satisfied by structured activity log events
- [X] T012 Objective: create service-layer skeletons and enforce route-to-service boundaries | Files: `backend/src/services/task_service.py`, `backend/src/services/focus_service.py`, `backend/src/services/timeline_service.py`, `backend/src/api/routes/__init__.py` | Validation: no business rules in route layer during code review | Testing: architecture test in `backend/tests/unit/test_route_service_boundary.py` | Logging: service entry/exit debug logs
- [X] T013 Objective: set up FastAPI app wiring, error handling, and dependency injection | Files: `backend/src/main.py`, `backend/src/api/dependencies.py`, `backend/src/api/error_handlers.py` | Validation: app boots and returns health response | Testing: integration test `backend/tests/integration/test_app_boot.py` | Logging: uncaught exception logging with request correlation id
- [X] T014 Objective: define frontend API client and typed service interfaces | Files: `frontend/src/services/httpClient.ts`, `frontend/src/services/taskApi.ts`, `frontend/src/services/focusApi.ts`, `frontend/src/services/timelineApi.ts`, `frontend/src/types/api.ts` | Validation: client methods map to contract endpoints | Testing: API client unit tests in `frontend/tests/services/apiClients.test.ts` | Logging: client error logging for failed calls

**Checkpoint**: Foundational architecture complete; user stories can proceed independently.

---

## Phase 3: User Story 1 - Create and Complete Daily Tasks (Priority: P1) 🎯 MVP

**Goal**: Let user create/update/complete tasks and review completed items in daily list.

**Independent Test**: Create multiple tasks, update one title, complete one task, and confirm status and completed ordering in UI/API.

### Tests for User Story 1

- [X] T015 [P] [US1] Objective: add API contract tests for `/tasks`, `/tasks/{taskId}`, `/tasks/{taskId}/complete` | Files: `backend/tests/contract/test_tasks_contract.py` | Validation: response schema/status match `contracts/openapi.yaml` | Testing: contract tests fail first then pass | Logging: assert activity log triggered for create/update/complete
- [X] T016 [P] [US1] Objective: add backend integration tests for task lifecycle workflows | Files: `backend/tests/integration/test_task_lifecycle.py` | Validation: persistence and state transitions follow spec | Testing: include invalid title and duplicate update edge paths | Logging: verify lifecycle events are logged

### Implementation for User Story 1

- [X] T017 [US1] Objective: implement task service business rules (create/update/complete) | Files: `backend/src/services/task_service.py` | Validation: enforces title constraints and completion transition rules | Testing: unit tests in `backend/tests/unit/test_task_service.py` | Logging: emit `task_created`, `task_updated`, `task_completed`
- [X] T018 [US1] Objective: implement task routes as thin controllers delegating to service | Files: `backend/src/api/routes/tasks.py` | Validation: routes only parse/map/delegate (no business branching) | Testing: route tests in `backend/tests/unit/test_task_routes.py` | Logging: request/response summary logs
- [X] T019 [US1] Objective: build task list UI with create/edit/complete actions | Files: `frontend/src/features/tasks/TaskList.tsx`, `frontend/src/features/tasks/TaskForm.tsx`, `frontend/src/features/tasks/taskStore.ts` | Validation: UI state updates match backend responses | Testing: component tests in `frontend/tests/features/tasks/TaskList.test.tsx` | Logging: log failed mutations to console telemetry hook
- [X] T020 [US1] Objective: add completed-work section ordered by completion sequence | Files: `frontend/src/features/tasks/CompletedTasksPanel.tsx` | Validation: completed tasks shown in correct order | Testing: UI test for ordering in `frontend/tests/features/tasks/CompletedTasksPanel.test.tsx` | Logging: N/A

**Checkpoint**: User Story 1 is independently functional and qualifies as MVP scope.

---

## Phase 4: User Story 2 - Focus on One Task at a Time (Priority: P2)

**Goal**: Enable single active focus session with start/stop flows and day rollover auto-stop behavior.

**Independent Test**: Start focus on one task, ensure second start is blocked, stop focus, and verify day-rollover auto-stop behavior.

### Tests for User Story 2

- [X] T021 [P] [US2] Objective: add API contract tests for `/focus/start` and `/focus/stop` conflict cases | Files: `backend/tests/contract/test_focus_contract.py` | Validation: 201/200/409 responses match contract | Testing: include no-active-session and already-active-session scenarios | Logging: assert focus start/stop events logged
- [X] T022 [P] [US2] Objective: add integration tests for single-active-session invariant and rollover stop | Files: `backend/tests/integration/test_focus_sessions.py` | Validation: exactly one active session invariant always holds | Testing: simulate local day boundary transition | Logging: verify `stop_reason=day_rollover` in logs/events

### Implementation for User Story 2

- [X] T023 [US2] Objective: implement focus service rules for start/stop and exclusivity | Files: `backend/src/services/focus_service.py` | Validation: prevents focus on completed task and concurrent sessions | Testing: unit tests in `backend/tests/unit/test_focus_service.py` | Logging: emit `focus_started`, `focus_stopped` with reason
- [X] T024 [US2] Objective: implement focus routes and response mapping | Files: `backend/src/api/routes/focus.py` | Validation: thin route layer with service delegation only | Testing: route tests in `backend/tests/unit/test_focus_routes.py` | Logging: request-level context logs
- [X] T025 [US2] Objective: implement rollover guard/worker to auto-stop active session at 23:59:59 local | Files: `backend/src/services/rollover_service.py`, `backend/src/main.py` | Validation: active session auto-stops at boundary and records event | Testing: deterministic time-based tests in `backend/tests/integration/test_rollover_service.py` | Logging: rollover stop events logged at info level
- [X] T026 [US2] Objective: add frontend focus controls and active-task indicator | Files: `frontend/src/features/focus/FocusControls.tsx`, `frontend/src/features/focus/ActiveFocusBanner.tsx`, `frontend/src/features/focus/focusStore.ts` | Validation: only one active focus shown and controls disabled appropriately | Testing: component tests in `frontend/tests/features/focus/FocusControls.test.tsx` | Logging: client-side error logging for focus command failures

**Checkpoint**: User Stories 1 and 2 are independently functional with focus invariants enforced.

---

## Phase 5: User Story 3 - Review Daily Activity Timeline (Priority: P3)

**Goal**: Show chronological daily activity timeline with deterministic tie-break ordering and clear completed-work review.

**Independent Test**: Execute task/focus actions, then verify timeline order by timestamp and fixed event priority for equal timestamps.

### Tests for User Story 3

- [X] T027 [P] [US3] Objective: add contract test for `/timeline/today` response shape and ordering fields | Files: `backend/tests/contract/test_timeline_contract.py` | Validation: payload matches `ActivityEvent` schema | Testing: include empty-day and populated-day cases | Logging: verify timeline query logs include selected day
- [X] T028 [P] [US3] Objective: add integration tests for timeline ordering, local-day grouping, and tie-break rules | Files: `backend/tests/integration/test_timeline_ordering.py` | Validation: event order follows spec FR-014 and FR-015 | Testing: same-timestamp multi-event scenario | Logging: validate ordering debug traces in test logs

### Implementation for User Story 3

- [X] T029 [US3] Objective: implement timeline service with local-day grouping and deterministic ordering | Files: `backend/src/services/timeline_service.py` | Validation: applies fixed event priority when timestamps tie | Testing: unit tests in `backend/tests/unit/test_timeline_service.py` | Logging: emit timeline generation metrics (count, duration)
- [X] T030 [US3] Objective: implement timeline route endpoint for daily review | Files: `backend/src/api/routes/timeline.py` | Validation: route delegates to service and maps response DTO | Testing: route tests in `backend/tests/unit/test_timeline_routes.py` | Logging: access logs include day and event count
- [X] T031 [US3] Objective: build timeline UI list for ordered daily activity | Files: `frontend/src/features/timeline/TimelineView.tsx`, `frontend/src/features/timeline/timelineStore.ts` | Validation: UI renders ordered events and empty state | Testing: component tests in `frontend/tests/features/timeline/TimelineView.test.tsx` | Logging: client warnings when timeline fetch fails
- [X] T032 [US3] Objective: add review summary panel for completed work sequence | Files: `frontend/src/features/timeline/CompletedWorkSummary.tsx` | Validation: summary order matches timeline completion events | Testing: UI test in `frontend/tests/features/timeline/CompletedWorkSummary.test.tsx` | Logging: N/A

**Checkpoint**: All user stories functional; end-of-day review fully supported.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, integration hardening, and release-readiness checks.

- [X] T033 [P] Objective: run full backend/frontend test suites and fix regressions | Files: `backend/tests/`, `frontend/tests/` | Validation: all tests pass in clean local setup | Testing: execute `pytest` and `npm test` | Logging: capture test run output artifacts
- [X] T034 Objective: perform end-to-end manual quickstart validation | Files: `specs/001-daily-work-tracker/quickstart.md` | Validation: quickstart steps reproducible from scratch | Testing: execute all core flows manually | Logging: verify activity log completeness per flow
- [X] T035 Objective: enforce dependency impact and risk checklist in release notes | Files: `specs/001-daily-work-tracker/research.md`, `specs/001-daily-work-tracker/plan.md` | Validation: each listed risk has implemented mitigation evidence | Testing: trace mitigation to tests/tasks | Logging: N/A
- [X] T036 Objective: verify rollback path by test migration downgrade/restore drill | Files: `backend/migrations/`, `specs/001-daily-work-tracker/quickstart.md` | Validation: downgrade and restore steps succeed locally | Testing: migration rollback rehearsal | Logging: migration rollback logs retained
- [X] T037 Objective: confirm no unauthorized schema changes beyond approved migrations | Files: `backend/migrations/versions/` | Validation: all schema changes mapped to approved plan/spec | Testing: schema diff check against baseline | Logging: N/A

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: start immediately.
- **Phase 2 (Foundational)**: depends on Setup completion; blocks all user stories.
- **Phase 3 (US1)**: depends on Foundational; recommended MVP delivery target.
- **Phase 4 (US2)**: depends on Foundational and reuses US1 task entity flows.
- **Phase 5 (US3)**: depends on Foundational and benefits from US1+US2 emitted events.
- **Phase 6 (Polish)**: depends on all selected user stories.

### User Story Dependencies

- **US1 (P1)**: independent after Foundational.
- **US2 (P2)**: independent after Foundational, requires Task entity from shared model.
- **US3 (P3)**: independent after Foundational, consumes activity events produced by US1/US2 behaviors.

### Within Each User Story

- Contract/integration tests first (fail initially).
- Service implementation before route/controller implementation.
- Frontend integration after API/service behavior is stable.
- Complete story-level validation before moving to next priority.

### Parallel Opportunities

- Setup tasks marked `[P]`: `T002`, `T003`, `T004`.
- Foundational tasks marked `[P]`: `T009`, `T010`.
- US1 parallel tests: `T015`, `T016`.
- US2 parallel tests: `T021`, `T022`.
- US3 parallel tests: `T027`, `T028`.
- Final validation parallelizable: `T033`.

---

## Parallel Example: User Story 2

```bash
Task: "T021 [US2] Contract tests for focus routes in backend/tests/contract/test_focus_contract.py"
Task: "T022 [US2] Integration tests for focus invariants in backend/tests/integration/test_focus_sessions.py"
Task: "T026 [US2] Frontend focus controls in frontend/src/features/focus/FocusControls.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Foundational)
3. Complete Phase 3 (US1)
4. Validate US1 independently and demo MVP value

### Incremental Delivery

1. Deliver US1 for immediate daily task tracking value.
2. Add US2 for focus discipline and session integrity.
3. Add US3 for end-of-day review and timeline clarity.
4. Finish with Phase 6 hardening, rollback drill, and risk closure.

### Validation Focus

- Every task includes direct validation steps and testing considerations.
- Logging/monitoring is explicitly addressed for service, route, and integration tasks where relevant.
- Architecture constraints (service-layer, thin routes, repository boundary) are enforced by dedicated tests and reviews.
