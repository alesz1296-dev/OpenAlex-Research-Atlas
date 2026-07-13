# Task Tracker

## Phase Exit Policy

Before a phase is marked complete, confirm:

- all in-scope tasks for that phase are either completed or explicitly deferred
- exit conditions in `phases.md` are satisfied
- manual validation has been performed and recorded
- automated validation has been run where available
- architecture ownership, DRY, and orthogonality have been reviewed
- `logs.md` records what was completed, what remains, and the validation outcome

## Phase 0: Foundation (Complete)

- Align root project documents with the revised LangChain-first and LangGraph-early plan.
- Define AI Reliability as the first OpenAlex domain slice.
- Establish evaluation, observability, and manual testing as core project requirements.
- Define public/private boundaries and `.gitignore` rules for local notes.
- Confirm the default stack and operational contracts for iteration.
- Document the Phase 0 SDD in `specs.md` with architecture, data model, interfaces, workflows, and validation.

## Phase 1: Data Model and Ingestion Foundation (In Progress)

- [x] Design Phase 1 data model (works, authors, topics, sources, citations, audit tables)
- [x] Create project structure (src/, tests/, scripts/)
- [x] Implement SQLAlchemy ORM models with detailed learning comments
- [x] Implement Pydantic validation schemas (Create, Read, Update patterns)
- [x] Setup database configuration and session management
- [x] Initialize Alembic for schema migrations
- [x] Create first database migration
- [x] Apply first database migration to configured PostgreSQL instance
- [x] Implement OpenAlex ingestion adapter (single work, fetch + normalize + upsert)
- [x] Add ingestion error tracking model and structured persistence
- [x] Implement Phase 1 ingestion policy for upserts, raw payloads, partial nested entities, and retry classification
- [x] Add retry execution flow for retryable ingestion errors
- [x] Write PostgreSQL-backed pytest fixtures and first ingestion tests
- [x] Document ingestion workflow and manual test procedures
- [x] Add production API foundation: app entrypoint, health/readiness/version/metrics, request IDs, structured logs, normalized errors
- [x] Add retrieval-before-generation API contract and first keyword retrieval service
- [x] Add Azure OpenAI inference adapter, disabled by default and mockable in tests
- [x] Add local retrieval evaluation harness with seed dataset
- [x] Add Prometheus/Grafana local observability wiring
- [x] Add first GitHub Actions CI checkpoint for Ruff, compile/import checks, Alembic, and pytest
- [x] Separate local development and test PostgreSQL databases
- [x] Validate real one-work ingestion and re-ingestion against PostgreSQL
- [x] Validate local Docker stack for API, PostgreSQL, Prometheus, and Grafana
- [x] Complete Phase 1 architecture ownership review

## Next

- Note for later phases: if richer author/topic metadata is needed, add explicit enrichment flows that fetch full author/topic endpoints instead of relying only on nested work payload fragments.
- Phase 1 exit conditions are satisfied; prepare closeout commit and move implementation focus to Phase 2.
- Define LangChain document mapping for OpenAlex works.
- Define the first LangGraph research workflow state.
- Define manual test scripts for ingestion, retrieval, and workflow execution.
- Define first API workflow.

## Phase 2 Progress Notes

- `P2-01`: `Work -> LangChain Document` mapper implemented.
- `P2-02`: retrieval request/response contract expanded with filters, result counts, and richer evidence fields.
- `P2-03`: retrieval service tests added for ranking and filter behavior.
- `P2-04`: ownership review completed for API, evaluation, and inference; inference should consume the full `RetrievalResponse`.
- `P2-05`: retrieval manual runbook added for keyword, year filter, open-access filter, and citation inspection.

## Later

- Close Phase 1 after successful manual validation and PostgreSQL-backed test execution.
- Add implementation tickets by spec ID.
- Add evaluation dataset tasks.
- Add deployment hardening tasks.
- Add MCP tool contracts after retrieval exists.

## Phase-by-Phase Planning Queue

### Progressive CI/CD Tracker

- Phase 1 CI: lint, compile/import, PostgreSQL service, Alembic upgrade, ingestion tests.
- Phase 2 CI: retrieval tests, metadata filter tests, vector-store checks.
- Phase 3 CI: mocked LangGraph state transition and workflow tests.
- Phase 4 CI: local evaluation smoke checks and stable regression thresholds.
- Phase 5 CI: `/metrics` and structured logging contract checks.
- Phase 6 CI: Kubernetes manifest validation and Helm template rendering.
- Phase 7 CI: Argo CD Application manifest validation.
- Phase 8 CI: Terraform fmt, validate, and non-applying plan.
- Phase 9 CI/CD: release promotion, environment approvals, rollback documentation, cloud apply gates.

### Phase 2 Planning Tasks

- Specify LangChain document mapping contracts for ingested works.
- Specify retrieval interfaces, filters, and evidence output shape.
- Define `pgvector` storage and embedding validation approach.
- Define retrieval service ownership so API, AI, and evaluation code do not duplicate retrieval queries.
- Define Phase 2 exit conditions and validation cases before implementation.

### Phase 3 Planning Tasks

- Specify LangGraph workflow state and node contracts.
- Define grounded response format and failure-handling behavior.
- Define workflow dependency boundaries between retrieval, inference, grounding checks, and observability.
- Define Phase 3 exit conditions and validation cases before implementation.

### Phase 4 Planning Tasks

- Expand evaluation datasets, metrics, and regression expectations from the local retrieval seed.
- Define evaluation run outputs and acceptance thresholds.
- Define Phase 4 exit conditions and validation cases before implementation.

### Phase 5 Planning Tasks

- Expand required observability records across ingestion, retrieval, Azure OpenAI calls, and workflows.
- Define logging/tracing minimum fields and inspection workflow.
- Decide whether direct Prometheus counter imports remain acceptable or whether a small observability facade is needed.
- Define Phase 5 exit conditions and validation cases before implementation.

### Phase 6 Planning Tasks

- Specify local Kubernetes architecture with raw manifests first.
- Specify Helm chart structure, values, and validation commands.
- Define local cluster setup, migration job behavior, smoke tests, and teardown.
- Define Phase 6 exit conditions and validation cases before implementation.

### Phase 7 Planning Tasks

- Specify Argo CD local installation and Application manifests.
- Define GitOps sync, diff, rollback, and drift inspection workflows.
- Define Phase 7 exit conditions and validation cases before implementation.

### Phase 8 Planning Tasks

- Specify AWS Terraform modules for ECR, IAM/OIDC, logs, and low-cost runtime.
- Define low-cost deployment assumptions, teardown steps, and cost guardrails.
- Define Phase 8 exit conditions and validation cases before implementation.

### Phase 9 Planning Tasks

- Specify release promotion workflows that consolidate existing tests, Docker, Helm, and Terraform checks.
- Define deployment approval gates and required secrets.
- Define Phase 9 exit conditions and validation cases before implementation.

### Phase 10 Planning Tasks

- Specify MCP tool surface, tool contracts, and response formats.
- Define minimal safe tool set for first exposure.
- Define Phase 10 exit conditions and validation cases before implementation.

### Phase 11 Planning Tasks

- Specify deployment packaging, environment rules, and production safeguards.
- Define CI/CD deployment gates and operational smoke tests.
- Define Phase 11 exit conditions and validation cases before implementation.
