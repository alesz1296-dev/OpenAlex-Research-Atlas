# Task Tracker

## Phase Exit Policy

Before a phase is marked complete, confirm:

- all in-scope tasks for that phase are either completed or explicitly deferred
- exit conditions in `phases.md` are satisfied
- manual validation has been performed and recorded
- automated validation has been run where available
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

## Next

- Resume with manual validation of Phase 1 using `src/ingestion/manual_test.md`.
- Test single-work ingestion against a real database.
- Review one-work upsert behavior against real OpenAlex payloads and adjust any field mappings that are too sparse or too aggressive.
- Validate Docker-based local development for PostgreSQL, API, Prometheus, and Grafana.
- Define the first CI checkpoint: run Ruff, import/compile checks, Alembic migrations, and at least one ingestion-focused pytest test.
- Define LangChain document mapping for OpenAlex works.
- Define the first LangGraph research workflow state.
- Define manual test scripts for ingestion, retrieval, workflow execution, and private-note exclusion.
- Define first API workflow.

## Later

- Close Phase 1 after successful manual validation and PostgreSQL-backed test execution.
- Add GitHub Actions after Dockerized local development and the first ingestion tests are stable.
- Add implementation tickets by spec ID.
- Add evaluation dataset tasks.
- Add deployment hardening tasks.
- Add MCP tool contracts after retrieval exists.

## Phase-by-Phase Planning Queue

### Phase 2 Planning Tasks

- Specify LangChain document mapping contracts for ingested works.
- Specify retrieval interfaces, filters, and evidence output shape.
- Define `pgvector` storage and embedding validation approach.
- Define Phase 2 exit conditions and validation cases before implementation.

### Phase 3 Planning Tasks

- Specify LangGraph workflow state and node contracts.
- Define grounded response format and failure-handling behavior.
- Define Phase 3 exit conditions and validation cases before implementation.

### Phase 4 Planning Tasks

- Expand evaluation datasets, metrics, and regression expectations from the local retrieval seed.
- Define evaluation run outputs and acceptance thresholds.
- Define Phase 4 exit conditions and validation cases before implementation.

### Phase 5 Planning Tasks

- Expand required observability records across ingestion, retrieval, Azure OpenAI calls, and workflows.
- Define logging/tracing minimum fields and inspection workflow.
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

- Specify GitHub Actions workflows for tests, Docker, Helm, and Terraform.
- Define deployment approval gates and required secrets.
- Define Phase 9 exit conditions and validation cases before implementation.

### Phase 10 Planning Tasks

- Specify local-only private note ingestion and privacy gating rules.
- Define exclusion validation for git and public workflows.
- Define Phase 10 exit conditions and validation cases before implementation.

### Phase 11 Planning Tasks

- Specify MCP tool surface, tool contracts, and response formats.
- Define minimal safe tool set for first exposure.
- Define Phase 11 exit conditions and validation cases before implementation.

### Phase 12 Planning Tasks

- Specify deployment packaging, environment rules, and production safeguards.
- Define CI/CD deployment gates and operational smoke tests.
- Define Phase 12 exit conditions and validation cases before implementation.
