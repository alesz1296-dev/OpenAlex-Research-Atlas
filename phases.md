# Project Phases

## Phase 0: Foundation

Goal:
Create the project operating system and LangChain-first architecture before writing application code.

Deliverables:

- `README.md`
- `architecture.md`
- `working-standard.md`
- `specs.md`
- `task.md`
- `logs.md`
- `ASSISTANTS.md`
- `.gitignore`
- `private/` local note area
- default stack
- AI Reliability domain slice
- manual and automated testing standard

Scope:

- Document project intent, architecture, and development rules.
- Define the default stack and AI Reliability research slice.
- Establish public/private note boundaries and git exclusion rules.
- Set the LangChain-first plus LangGraph-early project approach.
- Capture manual and automated testing standards early.
- Keep project docs as the source of truth for phase planning.
- Record the Phase 0 Software Design Document in `specs.md`.

## Phase 1: LangChain OpenAlex Ingestion

Goal:
Use LangChain-compatible document abstractions while ingesting AI Reliability works from OpenAlex.

Operational sequencing for this phase:

- Start with Dockerized local development for PostgreSQL and the application runtime.
- Add CI after one-work ingestion, Alembic migrations, and the first ingestion-focused tests are stable enough to enforce in pull requests.

## Phase 2: LangChain Retrieval Core

Goal:
Implement searchable, filterable, citation-aware, and semantic scholarly retrieval with LangChain and `pgvector`.

## Phase 3: LangGraph Research Workflow

Goal:
Add the first stateful research workflow: question, retrieval, citation inspection, synthesis, grounding validation, and cited response.

## Phase 4: Evaluation

Goal:
Measure retrieval quality and answer grounding with repeatable tests.

## Phase 5: Observability

Goal:
Track API requests, ingestion runs, retrieval traces, LangChain calls, LangGraph transitions, failures, latency, and eval history.

## Phase 6: Private Notes Integration

Goal:
Index local-only private notes for personal workflows while keeping them excluded from git and public exports.

## Phase 7: MCP Research Tools

Goal:
Expose selected search, lookup, synthesis, workflow, and evaluation capabilities through MCP.

## Phase 8: Production Hardening

Goal:
Add deployment, observability, authentication, and operational safety.
