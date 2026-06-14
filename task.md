# Task Tracker

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
- [ ] Apply first database migration to configured PostgreSQL instance
- [x] Implement OpenAlex ingestion adapter (single work, fetch + normalize + upsert)
- [x] Add ingestion error tracking model and structured persistence
- [x] Implement Phase 1 ingestion policy for upserts, raw payloads, partial nested entities, and retry classification
- [x] Add retry execution flow for retryable ingestion errors
- [x] Write PostgreSQL-backed pytest fixtures and first ingestion tests
- [x] Document ingestion workflow and manual test procedures

## Next

- Apply the PostgreSQL migrations locally and test single-work ingestion against a real database.
- Review one-work upsert behavior against real OpenAlex payloads and adjust any field mappings that are too sparse or too aggressive.
- Add Docker-based local development for PostgreSQL and the app so Phase 1 work runs in a consistent environment.
- Define the first CI checkpoint: run Ruff, import/compile checks, Alembic migrations, and at least one ingestion-focused pytest test.
- Define LangChain document mapping for OpenAlex works.
- Define the first LangGraph research workflow state.
- Define manual test scripts for ingestion, retrieval, workflow execution, and private-note exclusion.
- Define first API workflow.

## Later

- Add GitHub Actions after Dockerized local development and the first ingestion tests are stable.
- Add implementation tickets by spec ID.
- Add evaluation dataset tasks.
- Add deployment hardening tasks.
- Add MCP tool contracts after retrieval exists.
