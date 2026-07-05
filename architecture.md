# Architecture

## System Purpose

OpenAlex Research Atlas is a production-grade scholarly research intelligence platform that combines:

- public scholarly metadata from OpenAlex
- local enriched content such as abstracts, notes, and derived chunks
- LangChain workflows for retrieval, synthesis, comparison, and evaluation
- LangGraph workflows for stateful research processes

## Architectural Principles

- Spec-driven development before implementation.
- Keep private learning material outside tracked project artifacts.
- Production-grade boundaries from the beginning: typed contracts, testability, logging, observability, and modular services.
- DRY by ownership, not by premature abstraction: shared behavior should move into one owner only after repetition proves stable.
- Orthogonal modules: ingestion, retrieval, inference, evaluation, observability, persistence, API, and deployment should each have clear reasons to change.
- API routes should stay thin and delegate business behavior to service modules.
- Domain services should expose typed inputs and outputs rather than leaking raw framework details across boundaries.
- OpenAlex is the external source of truth for scholarly metadata.
- LangChain is part of the core architecture from the first implemented AI workflow.
- LangGraph is introduced early once retrieval can support a meaningful research workflow.
- Private learning material is not a product feature and should not enter retrieval, evaluation, or deployment artifacts.

## Default Stack

- Backend: `FastAPI`
- Language: `Python`
- Validation and contracts: `Pydantic`
- Database: `PostgreSQL`
- Vector search: `pgvector`
- Migrations: `Alembic`
- Data access: `SQLAlchemy`
- External corpus: `OpenAlex API`
- AI framework: `LangChain`
- Agent and workflow framework: `LangGraph`
- MCP layer: Python MCP server after the first retrieval workflow exists
- Testing: `pytest` plus documented manual testing
- Observability: structured logs, request IDs, LangChain run metadata, retrieval traces, LangGraph execution records, and eval run records
- Frontend: deferred until API and workflow shape are clear; likely `React` or `Next.js`
- Deployment: Docker first, cloud deployment later

## High-Level Components

```text
User
  -> Web UI / API Client
  -> API Service
  -> Application Services
     -> LangChain OpenAlex Ingestion Service
     -> LangChain Retrieval and Search Service
     -> LangGraph Research Workflow Service
     -> AI Synthesis Service
     -> Evaluation Service
     -> Observability Service
  -> PostgreSQL + pgvector
  -> Local file storage for cached raw documents
```

## Module Boundaries

The codebase should preserve these module responsibilities as it grows:

- `src/api`: FastAPI app, routes, request/response wiring, dependency injection, and HTTP error shape.
- `src/core`: cross-cutting configuration, logging, request IDs, and metrics setup.
- `src/database`: SQLAlchemy models, database sessions, Alembic migrations, and SQL reference material.
- `src/ingestion`: OpenAlex fetch/normalize/upsert workflow and ingestion retry behavior.
- `src/retrieval`: retrieval services and evidence/citation response construction.
- `src/ai`: provider adapters and inference services, including Azure OpenAI boundaries.
- `src/evaluation`: local evaluation harnesses and scoring logic.
- `scripts`: runnable developer workflows that compose services without owning business rules.
- `observability`: Prometheus and Grafana configuration, dashboards, and future telemetry setup.

Dependency direction should stay mostly one-way:

```text
api -> services -> database models/session
services -> core config/observability
evaluation -> retrieval service contracts
scripts -> services
```

Avoid reverse dependencies such as database modules importing API code, retrieval importing API routes, or provider adapters owning retrieval logic.

## DRY and Orthogonality Rules

DRY should protect meaning, not erase useful separation. Similar-looking code may stay separate when it belongs to different concepts, such as API contracts versus ORM persistence models.

Use these rules:

- Prefer one owner for one concept: OpenAlex normalization belongs in ingestion, citation-ready evidence belongs in retrieval, model calls belong in AI services, metrics setup belongs in core/observability.
- Avoid duplicated business decisions across routes, scripts, and tests. If a rule affects behavior, put it in a service and test it there.
- Keep infrastructure concerns explicit: Docker, Kubernetes, Helm, Argo CD, Terraform, and CI/CD should be documented and implemented as real tools, not hidden behind generic wrappers.
- Do not introduce broad helper layers just to reduce a few repeated lines; add abstractions when they remove real coupling or repeated decisions.
- Keep public/private boundaries orthogonal to retrieval and AI behavior. Private learning material must stay outside public OpenAlex workflows.

## Current Architecture Review Notes

- The current package layout is healthy for Phase 1: API, core, database, ingestion, retrieval, AI, and evaluation are separated.
- Routes still perform some direct ORM reads for simple list/detail endpoints. This is acceptable during Phase 1, but Phase 2 should move retrieval-oriented queries into service/query modules.
- Observability counters are currently imported directly into services. This is acceptable while the metrics set is small, but Phase 5 should introduce a cleaner observability facade if metrics calls become noisy.
- SQLAlchemy models and Pydantic schemas are intentionally separate. They should not be merged even when fields overlap, because they represent different boundaries: persistence versus API contracts.
- The SQL reference file should remain aligned with Alembic migrations and the live PostgreSQL schema so it stays useful as a learning artifact.

## First Research Domain

The first domain slice is AI Reliability.

Initial topics include:

- retrieval-augmented generation
- AI evaluation
- agent systems
- tool use
- observability for AI systems
- prompt injection
- AI safety
- production AI engineering

## Initial Data Domains

- works
- authors
- institutions
- topics
- sources
- citations
- local documents
- document chunks
- embeddings
- evaluation runs
- research sessions
- LangChain run records
- LangGraph execution records
- retrieval traces

## Proposed Storage Strategy

### Primary database

- PostgreSQL for structured metadata
- `pgvector` for embeddings and semantic retrieval

### Local file storage

- cached API payloads
- optional PDFs or exported text

## Boundary Between Public Repo and Private Learning

### Public

- code
- tests
- architecture
- specs
- sanitized sample data
- deployment and ops documentation
- public-safe manual testing reports
- public-safe evaluation methodology

### Private

- personal notes
- paper summaries copied from reading sessions
- raw learning references
- reflective logs not intended for publication
- framework comparison notes
- prompt experiments that include private context

Private material is local context only. It is not an indexed product data source, not a planned implementation phase, and not part of public documentation beyond this exclusion rule.

## AI Workflow Strategy

LangChain is the default implementation path for AI-facing workflows. Raw provider calls may exist only behind small adapters for testing, mocking, or comparison, but they should not become the main application path.

The first LangGraph workflow should follow this shape:

```text
research question
  -> retrieve evidence
  -> inspect citations
  -> synthesize answer
  -> validate grounding
  -> produce cited response
```

## Evaluation and Observability

Evaluation and observability are core AI engineering topics in this project, not deferred polish.

Evaluation must cover:

- retrieval quality
- answer grounding
- hallucination resistance
- workflow regressions

Observability must cover:

- API request IDs
- ingestion runs
- LangChain call metadata
- LangGraph node transitions
- retrieval traces
- latency and failures
- token and cost estimates when available
- evaluation run history

## Evolution Path

### Phase 0

Project foundation, specification system, LangChain-first architecture, logging, and private/public boundaries.

The Phase 0 Software Design Document is defined in `specs.md` and defines the foundation architecture, data model concepts, interface contracts, workflow expectations, and validation strategy.

### Phase 1

LangChain OpenAlex ingestion and database modeling.

Current Phase 1 implementation note:

- the current ingestion slice is intentionally one-work-at-a-time for learning and traceability
- PostgreSQL is the primary database target
- ingestion persists audit and failure records as first-class tables
- retry execution now exists at the service layer, with full retry workflows deferred until after manual validation

### Phase 2

LangChain retrieval and citation-aware academic search.

### Phase 3

LangGraph research workflow for grounded synthesis, comparison, and question answering.

### Phase 4

Evaluation workflows and research quality controls.

### Phase 5

Observability for API, ingestion, retrieval, LangChain calls, LangGraph workflows, and eval runs.

### Phase 6

Local Kubernetes and Helm.

### Phase 7

Argo CD GitOps.

### Phase 8

AWS Terraform low-cost deployment.

### Phase 9

CI/CD release gates and promotion.

### Phase 10

MCP research tools.

### Phase 11

Production hardening and operations.
