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

### Commit Log

- No project commits recorded yet.
