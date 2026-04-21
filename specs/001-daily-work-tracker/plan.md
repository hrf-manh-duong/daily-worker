# Implementation Plan: Daily Work Tracker MVP

**Branch**: `001-daily-work-tracker` | **Date**: 2026-04-21 | **Spec**: `/specs/001-daily-work-tracker/spec.md`
**Input**: Feature specification from `/specs/001-daily-work-tracker/spec.md`

## Summary

Build a local-first, single-user MVP for daily work tracking with explicit separation
between React frontend, Python backend API, and PostgreSQL persistence. The design
enforces service-layer business logic, thin controllers/routes, repository-based data
access separation, auditable activity logging, minimal dependencies, and a simple rollback
path for schema/data and release behavior.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12 (backend), Node.js 20 + TypeScript (frontend)  
**Primary Dependencies**: FastAPI, Uvicorn, Pydantic, SQLAlchemy, psycopg, React, Vite  
**Storage**: PostgreSQL 16 (local instance; browse/manage with DBeaver)  
**Testing**: pytest (backend), Vitest + React Testing Library (frontend), API contract checks  
**Target Platform**: Local Linux desktop development environment  
**Project Type**: Web application (frontend + backend service + relational database)  
**Performance Goals**: p95 API read latency <250ms locally; UI refresh for timeline <1s for 500 events/day  
**Constraints**: Single-user only, minimal dependencies, strict service-layer architecture, no schema changes without approval  
**Scale/Scope**: 1 active user, daily task/focus/event volume under 1,000 events/day

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] Service-layer ownership is explicit for each business capability (no business logic in controllers).
- [ ] Controller responsibilities are limited to transport concerns and service delegation.
- [ ] Reuse scan completed and documented for existing modules/utilities before adding new code.
- [ ] Validation strategy is defined for all external inputs and critical invariants.
- [ ] Module boundaries and allowed inter-module dependencies are documented.
- [ ] If schema changes are proposed, explicit approval evidence is linked; otherwise confirm no schema change.
- [x] Service-layer ownership is explicit for each business capability (no business logic in controllers).
- [x] Controller responsibilities are limited to transport concerns and service delegation.
- [x] Reuse scan completed and documented for existing modules/utilities before adding new code.
- [x] Validation strategy is defined for all external inputs and critical invariants.
- [x] Module boundaries and allowed inter-module dependencies are documented.
- [x] If schema changes are proposed, explicit approval evidence is linked; otherwise confirm no schema change.

## Project Structure

### Documentation (this feature)

```text
specs/001-daily-work-tracker/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   ├── services/
│   ├── repositories/
│   ├── domain/
│   ├── db/
│   └── logging/
├── migrations/
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── services/
│   └── types/
└── tests/
```

**Structure Decision**: Use web-application split with explicit boundaries:
frontend handles view state and user interactions; backend routes are thin and delegate
to services; repositories isolate all database access; persistence remains behind service
interfaces. This enforces constitution rules and enables isolated tests.

## Complexity Tracking

No constitution violations identified. Complexity accepted due to mandatory separation of
frontend/backend/persistence and explicit service/repository boundaries.

## Phase 0 Research Output

- Research document: `/specs/001-daily-work-tracker/research.md`
- All technical unknowns resolved without `NEEDS CLARIFICATION` items.
- Dependency impact analysis completed with mitigation actions for each dependency.
- Risk analysis completed with likelihood/impact/response coverage for architecture,
  timeline ordering, day rollover behavior, migration safety, and dependency growth.

## Phase 1 Design Output

- Data model: `/specs/001-daily-work-tracker/data-model.md`
- API contracts: `/specs/001-daily-work-tracker/contracts/openapi.yaml`
- Local runbook: `/specs/001-daily-work-tracker/quickstart.md`
- Agent context updated via `.specify/scripts/bash/update-agent-context.sh cursor-agent`

## Post-Design Constitution Re-Check

- [x] Service-layer ownership remains explicit in planned modules (`backend/src/services`).
- [x] Controllers/routes remain thin and contain no business logic (`backend/src/api/routes`).
- [x] Reuse-first requirement addressed by dedicated reuse scan in foundational planning.
- [x] Validation rules defined in data model and contract schemas.
- [x] Module boundaries documented across frontend/backend/repository layers.
- [x] Schema governance enforced with explicit approval gate and rollback path.
