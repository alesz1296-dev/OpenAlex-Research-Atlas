# Session Logs

## 2026-06-13

### Session: project foundation bootstrap

- Established OpenAlex Research Atlas as the working project concept.
- Created root project documents for spec-driven development.
- Defined the private-note boundary and local-only academic notes policy.
- Added assistant and git workflow rules to the project root.

### Commit Log

- No project commits recorded yet.

## 2026-06-14

### Session: LangChain-first project plan implementation

- Updated the project plan to make LangChain part of the core implementation from Phase 1.
- Added LangGraph as an early workflow layer for stateful research workflows.
- Set AI Reliability as the first OpenAlex domain slice.
- Made evaluation, observability, and manual testing explicit project requirements.
- Preserved the public research-platform positioning and private local academic learning layer.
- Closed Phase 0 foundation: verified root docs, confirmed AI Reliability domain slice, validated public/private boundaries and `.gitignore`, and documented the Phase 0 SDD in `specs.md`.

### Session: Phase 1 Data Model and SQLAlchemy Learning

- Designed complete Phase 1 data model: works, authors, topics, sources, citations, ingestion_runs, api_logs.
- Created full project structure: src/, tests/, scripts/ with proper package organization.
- Implemented SQLAlchemy ORM models (models.py) with detailed learning comments covering:
  - Declarative base and column types
  - Relationships (one-to-many, many-to-many)
  - Constraints and indexes
  - Foreign keys with CASCADE deletion
- Implemented Pydantic schemas (schemas.py) with validation patterns:
  - Create/Update/Read schemas for each entity
  - Minimal vs. Full response schemas for performance
  - orm_mode configuration for ORM object serialization
- Setup database layer:
  - config.py: Pydantic-based environment configuration
  - session.py: connection pooling and FastAPI dependency injection
  - requirements.txt: all Phase 1 dependencies (FastAPI, SQLAlchemy, Pydantic, Alembic)
  - .env.example: configuration template for local development
- Created API routes stub (routes.py) with learning notes for future implementation.
- Added Alembic migration placeholder with learning notes on schema versioning.

### Session: Phase 1 migration repair and initial revision

- Fixed SQLAlchemy mapper configuration by correcting the `Topic.works` relationship target.
- Updated settings to use `pydantic-settings`, load `.env` and `.env.local`, and tolerate the local `DEBUG=release` shell value.
- Updated Pydantic schemas to use `from_attributes` for Pydantic v2 ORM serialization.
- Repaired the Alembic revision template and created the initial migration file:
  - `alembic/versions/dcad9f50b14c_create_initial_schema.py`
- Validated the migration offline with `alembic upgrade head --sql`.
- Confirmed live `alembic revision --autogenerate` / `upgrade` is still blocked by invalid PostgreSQL credentials from the default placeholder `DATABASE_URL`.

### Session: Phase 1 one-work ingestion implementation

- Added explicit one-work OpenAlex ingestion with a small service layer in `src/ingestion/openalex.py`.
- Added a runnable learning script in `scripts/ingest_one_work.py`.
- Added an API endpoint for single-work ingestion in `src/api/routes.py`.
- Extended the ORM so `works` can reference `sources` through `source_id`.
- Added the `ingestion_errors` audit table and follow-up Alembic revision:
  - `alembic/versions/e71dd5afcc09_add_source_linkage_and_ingestion_errors.py`
- Added a PostgreSQL reference schema file that mirrors the ORM:
  - `src/database/postgres_schema_reference.sql`
- Validated imports, mapper configuration, and the full migration chain offline with `alembic upgrade head --sql`.

### Session: CI/CD sequencing plan update

- Mapped Docker-first delivery into Phase 1 planning:
  - local PostgreSQL and application runtime should be containerized before CI is enforced
- Mapped the first CI checkpoint after meaningful validation exists:
  - Ruff / import checks
  - Alembic migration execution
  - at least one ingestion-focused pytest test
- Updated `task.md`, `specs.md`, and `phases.md` so CI is planned as a follow-up to stable Dockerized local development rather than as empty early scaffolding.

### Session: Phase 1 ingestion policy implementation

- Implemented the first five Phase 1 ingestion decisions directly in code and documentation:
  - exact upsert behavior for works, authors, topics, and sources
  - recency treated as future batch ordering, not persistence logic
  - latest raw payload retained for persisted entities
  - partial nested source payloads accepted without clearing absent fields
  - retry classification recorded as structured metadata
- Added retry metadata to `ingestion_errors`:
  - `error_type`
  - `retryable`
- Added an ingestion policy reference:
  - `src/ingestion/policy.md`
- Added a follow-up migration for retry metadata:
  - `alembic/versions/ccb7e9e6f18a_add_ingestion_retry_metadata.py`

### Session: Phase 1 retry flow and learning test setup

- Added retry execution support in `src/ingestion/openalex.py` through `retry_ingestion_error`.
- Added PostgreSQL-backed pytest fixtures and first ingestion-focused tests:
  - `tests/conftest.py`
  - `tests/test_openalex_ingestion.py`
- Added a Dockerized PostgreSQL starter setup:
  - `docker-compose.yml`
- Added a manual learning runbook for migrations, ingestion, row inspection, and pytest:
  - `src/ingestion/manual_test.md`
- Updated `.env.example` with `TEST_DATABASE_URL` for PostgreSQL-backed tests.

### Session: Documentation sync before manual validation

- Updated root project docs to reflect the current Phase 1 checkpoint.
- Marked Phase 1 as implementation-complete enough to begin manual PostgreSQL validation.
- Recorded that the next session should resume with the manual learning runbook and live database verification.

## 2026-07-04

### Session: Spec-driven development governance update

- Strengthened the repo's spec-driven workflow so each phase now has:
  - core tasks
  - exit conditions
  - manual validation expectations
  - automated validation expectations
- Updated `working-standard.md`, `phases.md`, `specs.md`, `task.md`, and `README.md` to make phase completion criteria explicit.
- Added a phase-exit policy to `task.md` and a forward planning queue for Phases 2-8.

### Session: AI production system foundation

- Added the first production API foundation:
  - FastAPI app entrypoint
  - `/health`, `/ready`, `/version`, and `/metrics`
  - request IDs, structured JSON logging, normalized error responses, and pagination bounds
- Added Azure OpenAI as the first production inference target through a lazy, mockable service adapter.
- Added retrieval-before-generation contracts and a keyword retrieval endpoint for citation-ready evidence.
- Added a local retrieval evaluation harness and seed eval dataset that do not make paid model calls.
- Added Prometheus and Grafana local observability wiring through Docker Compose.
- Fixed the one-work ingestion control flow so fetched payloads are persisted again after the fetch step.
- Validation:
  - `python -m compileall src tests scripts` passed
  - `ruff check .` passed
  - `pytest -q` passed with 6 tests passing and 2 PostgreSQL integration tests skipped pending a configured database

### Session: Production infrastructure roadmap correction

- Updated the phase roadmap so production infrastructure is explicit rather than hidden under generic hardening.
- Added dedicated phases for:
  - local Kubernetes and Helm
  - Argo CD GitOps
  - AWS Terraform low-cost deployment
  - CI/CD and release gates
- Moved MCP and final production hardening later in the roadmap.
- Marked the configured PostgreSQL migration task as complete after the database reached Alembic revision `ccb7e9e6f18a`.

### Session: Architecture modularity and DRY review

- Reviewed current architecture docs, phase docs, task tracker, source layout, and module dependencies.
- Confirmed the current package layout is healthy for Phase 1:
  - API
  - core
  - database
  - ingestion
  - retrieval
  - AI provider adapter
  - evaluation
  - observability configuration
- Added explicit architecture rules for DRY, orthogonality, module ownership, dependency direction, and contract separation.
- Updated `architecture.md`, `working-standard.md`, `specs.md`, `phases.md`, and `task.md` so future phases must include architecture ownership checks before exit.
- Recorded Phase 1 follow-up design risks:
  - align Alembic/live PostgreSQL defaults with ORM and SQL reference expectations
  - keep routes thin as retrieval grows
  - avoid duplicated retrieval queries across API, AI, and evaluation layers
  - revisit direct metrics imports during Phase 5 if observability calls spread too much

### Session: Progressive CI/CD roadmap correction

- Clarified that CI/CD should be implemented gradually rather than as a single late phase.
- Updated Phase 1 to introduce the first CI checkpoint for lint, compile/import, PostgreSQL, Alembic, and ingestion tests.
- Added CI/CD maturity notes to Phases 2-8 so retrieval, workflow, evaluation, observability, Kubernetes, Argo CD, and Terraform checks are added when those capabilities exist.

## 2026-07-05 - Phase 1 CI checkpoint added

- Added the first GitHub Actions workflow at `.github/workflows/phase1-ci.yml`.
- The workflow now runs on pushes and pull requests with:
  - PostgreSQL 16 service container
  - `ruff check .`
  - `python -m compileall src scripts tests alembic`
  - import smoke checks for API, ingestion, AI, and evaluation modules
  - `alembic upgrade head`
  - `pytest -q`
- Marked the Phase 1 CI checkpoint task as complete in `task.md`.

## 2026-07-05 - Phase 1 architecture ownership tightened

- Refactored `POST /works` to delegate to `OpenAlexIngestionService` instead of writing `Work` rows directly from the route.
- Kept `POST /ingestion/works` as the explicit ingestion endpoint while making `POST /works` an ingestion-aligned alias rather than a second persistence owner.
- Migrated PostgreSQL test setup away from `Base.metadata.create_all()` and toward Alembic-owned schema setup using `upgrade head` / `downgrade base`.
- Added an API test that proves `POST /works` delegates to the ingestion service contract.

## 2026-07-05 - Phase 1 disposable test database validation

- Added a dedicated `postgres_test` Docker Compose service for local PostgreSQL tests.
- Updated `.env.example` and `src/ingestion/manual_test.md` so local `TEST_DATABASE_URL` uses `localhost:5433/openalex_research_test` instead of the development database.
- Added a pytest guard that skips destructive PostgreSQL integration tests in local development when `TEST_DATABASE_URL` equals `DATABASE_URL`.
- Added `ALEMBIC_DATABASE_URL` support in `alembic/env.py` so Alembic-owned test fixtures can target the disposable test database even if application settings were imported earlier.
- Validation passed:
  - `ruff check .`
  - `python -m compileall src scripts tests alembic`
  - full `pytest -q` against `postgres_test`, with 9 tests passing
- Phase 1 exit condition reassessment: all documented Phase 1 exit conditions are satisfied.
- Reframed Phase 9 as CI/CD release gates and promotion rather than initial CI/CD implementation.
- Updated `README.md`, `specs.md`, `phases.md`, `task.md`, `architecture.md`, and `logs.md`.

### Session: Remove private notes as implementation phase

- Removed Private Notes Integration as a standalone product phase.
- Renumbered MCP Research Tools to Phase 10 and Production Hardening to Phase 11.
- Updated design docs so private learning material remains local-only context, not a retrieval source, implementation track, or public documentation deliverable.
- Kept only the repository safety boundary: private material must stay out of tracked project artifacts.

### Commit Log

- No project commits recorded yet.

## 2026-07-12

### Session: Phase 2 retrieval manual validation runbook

- Added a dedicated Phase 2 retrieval manual runbook:
  - `src/retrieval/manual_test.md`
- Covered the first manual retrieval checks for:
  - keyword query
  - publication year filter
  - open-access filter
  - citation inspection
- Recorded the current Phase 2 progress notes in `task.md` so retrieval contract work, service tests, ownership review, and manual validation artifacts stay visible together.
