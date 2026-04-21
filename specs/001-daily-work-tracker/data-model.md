# Data Model: Daily Work Tracker MVP

## Entity: Task

### Fields
- `id` (UUID): unique task identifier
- `title` (string, 1..200 chars): task label shown in UI
- `status` (enum): `active`, `completed`
- `created_at` (timestamp with timezone): task creation time
- `completed_at` (timestamp with timezone, nullable): completion time
- `updated_at` (timestamp with timezone): last task metadata update

### Validation Rules
- `title` MUST be non-empty after trim.
- `title` length MUST be <= 200 characters.
- `completed_at` MUST be set only when `status = completed`.
- Completed tasks MUST NOT be started as active focus targets.

### State Transitions
- `active -> completed` (allowed by complete-task action)
- `completed -> active` (not allowed in MVP)

## Entity: FocusSession

### Fields
- `id` (UUID): unique focus session identifier
- `task_id` (UUID): reference to `Task.id`
- `started_at` (timestamp with timezone): session start
- `ended_at` (timestamp with timezone, nullable): session stop
- `state` (enum): `active`, `ended`
- `stop_reason` (enum): `manual`, `day_rollover`

### Validation Rules
- Exactly one `FocusSession` MAY have `state = active` at a time.
- `task_id` MUST reference an existing task with `status = active`.
- `ended_at` MUST be >= `started_at` when present.
- At day rollover, active sessions MUST stop at `23:59:59` local-time equivalent.

### State Transitions
- `active -> ended` (manual stop)
- `active -> ended` (automatic day rollover stop)
- `ended -> active` (not allowed; create a new session instead)

## Entity: ActivityEvent

### Fields
- `id` (UUID): unique event identifier
- `event_type` (enum): `task_created`, `focus_started`, `focus_stopped`, `task_completed`, `task_updated`
- `task_id` (UUID, nullable): associated task
- `focus_session_id` (UUID, nullable): associated focus session
- `occurred_at` (timestamp with timezone): event business time
- `local_day` (date): day bucket computed from user's local timezone at event time
- `payload` (jsonb): minimal metadata snapshot for UI rendering

### Validation Rules
- `event_type` MUST be one of the allowed values.
- `occurred_at` MUST always be present.
- `local_day` MUST match local timezone conversion of `occurred_at`.
- Timeline tie-break ordering MUST apply for equal `occurred_at` using:
  task_created, focus_started, focus_stopped, task_completed, task_updated.

## Relationships
- One `Task` to many `FocusSession`.
- One `Task` to many `ActivityEvent`.
- One `FocusSession` to many `ActivityEvent` (typically start/stop events).

## Derived Views
- **Daily Timeline**: ordered `ActivityEvent` records where `local_day = selected_day`,
  sorted by `occurred_at` then fixed event priority.
- **Completed Work Summary**: set of `Task` where `status = completed` and
  `completed_at` mapped to selected day.
