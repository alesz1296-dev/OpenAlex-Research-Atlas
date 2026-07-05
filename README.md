# OpenAlex Research Atlas

OpenAlex Research Atlas is a spec-driven, production-grade scholarly research platform built around OpenAlex as the primary reference database.

The system is intended to evolve from a local research platform into a deployed AI application. It will support ingestion of scholarly metadata, LangChain-based retrieval, LangGraph research workflows, citation-aware question answering, topic exploration, private annotations, evaluation workflows, and observability.

## Project Intent

- Use OpenAlex as the external scholarly knowledge backbone.
- Use LangChain from the first implemented AI and retrieval workflows.
- Introduce LangGraph early for stateful research workflows.
- Build the project through specification-driven development.
- Keep private learning material local and out of git.
- Maintain architecture, tasks, specs, and logs as first-class project artifacts.

## Required Root Documents

These Markdown files are part of the project operating system and must stay current:

- `README.md`
- `architecture.md`
- `working-standard.md`
- `specs.md`
- `task.md`
- `phases.md`
- `logs.md`
- `ASSISTANTS.md`

`specs.md` also contains the Phase 0 Software Design Document, capturing the foundation architecture, data model, interface contracts, workflows, and validation plan.

## Private Context

Private learning material is intentionally excluded from git and is not part of the product roadmap. It can include:

- reading notes
- paper summaries
- prompt experiments
- architecture reflections
- weekly learning logs

## Initial Thesis

This project builds a production-grade OpenAlex research platform while supporting private local learning outside tracked project artifacts.

The public repository should present the system as a serious scholarly research platform. Private local notes are personal context, not product functionality.

## Production Infrastructure Roadmap

The roadmap now treats infrastructure as explicit learning and implementation phases rather than hiding it inside general hardening:

- local Docker and PostgreSQL during Phase 1
- Prometheus and Grafana observability foundation during Phase 5
- local Kubernetes and Helm during Phase 6
- Argo CD GitOps during Phase 7
- low-cost AWS Terraform deployment during Phase 8
- CI/CD added gradually across phases, then release gates and promotion during Phase 9
- MCP and final production hardening after the platform and deployment paths are stable

CI/CD is a progressive thread, not a single late implementation phase. Each phase adds the automation that matches the capability being built, and Phase 9 consolidates those checks into release promotion and approval workflows.

## Current Status

- Phase 0 is complete.
- Phase 1 implementation is largely in place:
  - PostgreSQL schema and Alembic revisions
  - SQLAlchemy ORM models
  - one-work OpenAlex ingestion with explicit upsert behavior
  - structured ingestion error tracking and retry classification
  - PostgreSQL-backed pytest scaffolding
  - Docker starter setup for local PostgreSQL
- The first production API and AI-system foundation is now in place:
  - FastAPI app entrypoint with health, readiness, version, and Prometheus metrics endpoints
  - request IDs, structured JSON logging, normalized error responses, and pagination limits
  - Azure OpenAI inference adapter behind a service boundary, disabled by default for CI/local safety
  - retrieval-before-generation contracts for citation-ready evidence
  - local retrieval evaluation harness with no paid model calls
  - Docker Compose wiring for API, PostgreSQL, Prometheus, and Grafana
- The main remaining Phase 1 work is live validation:
  - apply migrations to a real PostgreSQL instance
  - run one real OpenAlex ingestion
  - inspect resulting rows manually
  - run the PostgreSQL ingestion tests end to end

## Delivery Model

This repository follows spec-driven development:

- phase goals and scope live in `phases.md`
- canonical requirements and validation live in `specs.md`
- implementation checkpoints live in `task.md`
- completed work and validation evidence are recorded in `logs.md`

Phases are not considered complete until their documented exit conditions and validation checks are satisfied.
