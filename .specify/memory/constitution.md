<!--
Sync Impact Report
- Version change: N/A -> 1.0.0
- Modified principles:
  - PRINCIPLE_1_NAME -> I. Service-Layer-Centric Architecture
  - PRINCIPLE_2_NAME -> II. Controller Thinness and Orchestration Only
  - PRINCIPLE_3_NAME -> III. Reuse-First Implementation
  - PRINCIPLE_4_NAME -> IV. Explicit and Enforced Code Style
  - PRINCIPLE_5_NAME -> V. Validation and Module Boundary Integrity
- Added sections:
  - Data and Change Control Constraints
  - Delivery Workflow and Quality Gates
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
  - ⚠ pending: .specify/templates/commands/*.md (directory not present in this repository)
  - ⚠ pending: README.md (not present in this repository)
  - ⚠ pending: docs/quickstart.md (not present in this repository)
- Follow-up TODOs:
  - None
-->
# Daily Worker Constitution

## Core Principles

### I. Service-Layer-Centric Architecture
All business behavior MUST be implemented in service-layer modules. Service modules MUST
own use-case orchestration, domain rules, and interaction sequencing across dependencies.
This ensures behavior remains testable, reusable, and independent from transport concerns.

### II. Controller Thinness and Orchestration Only
Controllers MUST limit responsibilities to request parsing, authentication context
resolution, delegation to services, and response mapping. Controllers MUST NOT contain
business decision logic, persistence rules, or cross-module orchestration. This keeps
transport adapters replaceable and prevents duplicated behavior.

### III. Reuse-First Implementation
Feature work MUST begin with discovery of existing utilities, services, and abstractions.
When equivalent functionality exists, teams MUST extend or compose it instead of
duplicating logic. New implementations MUST document why existing code could not be reused.
This preserves consistency and reduces long-term maintenance cost.

### IV. Explicit and Enforced Code Style
Code style rules MUST be explicit, automated, and consistently enforced through linting
and formatting tooling in local and CI workflows. Style exceptions MUST be narrowly scoped
and justified in code review. Uniform style improves readability, review quality, and
cross-team maintainability.

### V. Validation and Module Boundary Integrity
Every feature MUST define and enforce validation for all external inputs and critical
internal invariants. Modules MUST expose only well-defined interfaces, and consumers MUST
interact through those interfaces rather than internal implementation details. These rules
prevent invalid state propagation and protect architectural boundaries.

## Data and Change Control Constraints

Database schema changes (including migrations, table/column/index changes, or constraint
changes) MUST NOT be implemented without explicit stakeholder approval recorded in the
associated spec or PR. Any approved schema change MUST include rollback considerations and
impact analysis for dependent modules.

## Delivery Workflow and Quality Gates

Plans, specs, and task breakdowns MUST include checks that verify controller thinness,
service-layer ownership of logic, reuse opportunities, validation coverage, and module
boundary compliance. Pull requests MUST fail review if these checks are omitted or if
database schema changes appear without explicit approval evidence.

## Governance

This constitution supersedes conflicting local practices for architecture and delivery.
Amendments require: (1) a documented proposal, (2) reviewer approval, and (3) updates to
all impacted templates and guidance docs in the same change set.

Versioning policy:
- MAJOR: Removes or redefines existing principles in a backward-incompatible way.
- MINOR: Adds new principles or materially expands mandatory governance.
- PATCH: Clarifies wording without changing governance meaning.

Compliance review expectations:
- Every implementation plan MUST include constitution checks before and after design.
- Every feature spec MUST define validation requirements and architecture boundaries.
- Every task list MUST include explicit tasks for service placement, validation, and reuse.
- Every PR review MUST verify no unauthorized schema changes were introduced.

**Version**: 1.0.0 | **Ratified**: 2026-04-21 | **Last Amended**: 2026-04-21
