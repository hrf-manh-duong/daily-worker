# Research: Daily Work Tracker MVP

## Decision 1: Backend API Framework
- **Decision**: Use FastAPI + Uvicorn for the local backend service.
- **Rationale**: FastAPI provides strong request/response validation with low ceremony and
  keeps route handlers thin while delegating logic to services. It also has low
  dependency overhead for an MVP.
- **Alternatives considered**:
  - Flask: simpler core but requires additional choices for validation/docs patterns.
  - Django: heavier dependency footprint than needed for single-user local MVP.

## Decision 2: Persistence Access Pattern
- **Decision**: Use SQLAlchemy ORM with repository layer abstraction.
- **Rationale**: Repository pattern enforces separation between API transport and database
  concerns, aligning with constitution requirements and simplifying rollback and testing.
- **Alternatives considered**:
  - Raw SQL only: minimal dependencies but lower consistency and more repeated data-mapping logic.
  - SQLModel: convenient but overlaps concerns and is less explicit than a dedicated repository boundary.

## Decision 3: Activity Logging Model
- **Decision**: Persist activity events in a dedicated append-oriented `activity_events`
  table and derive timeline views from ordered events.
- **Rationale**: Event records preserve clear sequence of user actions and directly support
  timeline review requirements, including tie-break ordering and day grouping.
- **Alternatives considered**:
  - Compute timeline from task/focus tables only: loses fidelity for updates and stop reasons.
  - File-based logs: harder to query consistently from UI and less robust for ordering rules.

## Decision 4: Frontend Runtime and Build
- **Decision**: Use React + Vite + TypeScript.
- **Rationale**: Fast local startup, minimal build complexity, strong type feedback for API
  integration, and mature component/testing ecosystem.
- **Alternatives considered**:
  - Next.js: unnecessary server/runtime features for local-only MVP.
  - Plain React without TypeScript: lower setup effort but weaker contracts with backend payloads.

## Decision 5: Local Development Topology
- **Decision**: Run frontend and backend as separate local processes and connect to local PostgreSQL.
- **Rationale**: Matches explicit boundary requirement and makes component rollback
  straightforward (frontend and backend can revert independently if needed).
- **Alternatives considered**:
  - Monolithic server-rendered app: simpler deployment but weak boundary enforcement.
  - Embedded database (SQLite): lighter setup but conflicts with PostgreSQL requirement.

## Decision 6: Schema Change and Rollback Path
- **Decision**: Use migration scripts with explicit down migrations and pre-change backup snapshots.
- **Rationale**: Supports constitution governance for schema approval and gives a clear,
  testable rollback path in local development.
- **Alternatives considered**:
  - Manual SQL edits only: increases drift risk and rollback ambiguity.
  - No rollback scripts: unacceptable risk for data corruption during iteration.

## Dependency Impact Analysis

| Dependency | Purpose | Impact | Risk | Mitigation |
|-----------|---------|--------|------|------------|
| FastAPI | HTTP routing and validation | Medium | Route/service coupling if undisciplined | Enforce route thinness checks in tests/reviews |
| SQLAlchemy + psycopg | Data access and PostgreSQL connection | Medium | Incorrect session management, migration drift | Centralize session lifecycle in DB module and add integration tests |
| React + Vite | Desktop UI runtime and build tooling | Medium | State inconsistency vs backend timeline order | API contract tests and deterministic event ordering in backend |
| Pydantic | Input/output schema validation | Low | Over-validation noise for MVP | Keep strict on API boundaries only |
| pytest / Vitest | Test harnesses | Low | Increased setup effort | Minimal baseline suite focused on core flows only |

## Risk Analysis

| Risk | Likelihood | Impact | Response |
|------|------------|--------|----------|
| Business logic leaks into routes/controllers | Medium | High | Code review gate + route unit tests verifying pure delegation |
| Timeline ordering bugs on same timestamp | Medium | High | Apply fixed event priority in service layer + integration tests |
| Day rollover handling mismatch with user expectation | Medium | Medium | Enforce auto-stop at local 23:59:59 and cover with acceptance tests |
| Schema migration breaks local data | Low | High | Require migration approval, backup before migrate, tested down migration |
| Dependency bloat beyond MVP needs | Medium | Medium | Dependency budget review at PR time; reject non-essential packages |
