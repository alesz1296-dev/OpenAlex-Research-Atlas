# Architecture

## System Purpose

OpenAlex Research Atlas is a production-minded scholarly research intelligence platform focused first on public OpenAlex metadata and citation-aware AI research workflows.

The current product boundary is OpenAlex-first:

- ingest and normalize public scholarly metadata from OpenAlex
- retrieve citation-ready evidence from structured scholarly records
- generate grounded research answers only after retrieval has produced evidence
- measure retrieval, grounding, failures, latency, and regressions as first-class system behavior
- keep deployment, CI/CD, metrics, dashboards, and operational checks visible as production learning artifacts

Future local documents or public-safe enriched content may be added after the OpenAlex retrieval path is reliable. Private learning notes are not part of product retrieval, evaluation, deployment, or public documentation.

## Architectural Principles

- Spec-driven development before implementation.
- Keep private learning material outside tracked project artifacts.
- Production-grade boundaries from the beginning: typed contracts, testability, logging, observability, and modular services.
- DRY by ownership, not by premature abstraction: shared behavior should move into one owner only after repetition proves stable.
- Orthogonal modules: ingestion, retrieval, inference, evaluation, observability, persistence, API, and deployment should each have clear reasons to change.
- API routes should stay thin and delegate business behavior to service modules.
- Domain services should expose typed inputs and outputs rather than leaking raw framework details across boundaries.
- OpenAlex is the external source of truth for scholarly metadata.
- LangChain supports document, retriever, embedding, and retrieval pipeline abstractions; it does not own application policy.
- LangGraph owns workflow orchestration once retrieval can support a meaningful research process.
- Azure OpenAI calls must stay behind inference service boundaries and must consume retrieved evidence rather than raw database rows.
- Evaluation, observability, metrics, and CI/CD are production system requirements, not optional polish.
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
- Production inference provider: `Azure OpenAI`
- MCP layer: Python MCP server after the first retrieval workflow exists
- Testing: `pytest` plus documented manual testing
- Observability: Prometheus, Grafana, structured logs, request IDs, retrieval traces, inference metrics, LangGraph execution records, and eval run records
- Frontend: deferred until API and workflow shape are clear; likely `React` or `Next.js`
- Deployment: Docker first, local Kubernetes/Helm and Argo CD next, low-cost AWS Terraform later

## High-Level Components

```text
User
  -> Web UI / API Client
  -> API Service
  -> Application Services
     -> OpenAlex Ingestion Service
     -> LangChain Retrieval and Evidence Service
     -> LangGraph Research Workflow Service
     -> AI Inference Service
     -> Evaluation Harness
     -> Observability and Metrics
  -> PostgreSQL + pgvector
  -> Prometheus + Grafana
```

## Production AI Architecture

The system is intentionally layered so the LLM is never the source of truth.

- Ingestion creates trustworthy, auditable scholarly records from OpenAlex.
- Retrieval converts stored works into citation-ready evidence with provenance.
- Inference consumes retrieval output and cites evidence; it should not query persistence directly.
- LangGraph coordinates multi-step research workflows after retrieval and inference contracts are stable.
- Evaluation measures retrieval quality, citation coverage, groundedness, unsupported claims, and regressions.
- Observability records request IDs, ingestion runs, retrieval latency, inference calls, token usage, workflow failures, eval runs, and dashboard-visible metrics.

The production direction is retrieval-before-generation. If retrieval cannot produce stable evidence, the system should return a retrieval or grounding status that makes that limitation explicit instead of producing an unsupported answer.

## Module Boundaries

The codebase should preserve these module responsibilities as it grows:

- `src/api`: FastAPI app, routes, request/response wiring, dependency injection, and HTTP error shape.
- `src/core`: cross-cutting configuration, logging, request IDs, and metrics setup.
- `src/database`: SQLAlchemy models, database sessions, Alembic migrations, and SQL reference material.
- `src/ingestion`: OpenAlex fetch/normalize/upsert workflow and ingestion retry behavior.
- `src/retrieval`: LangChain document mapping, retriever composition, evidence ranking, filters, and citation-ready response construction.
- `src/ai`: provider adapters, inference prompts, Azure OpenAI configuration, token/call metrics, and model-call policy.
- `src/evaluation`: local evaluation datasets, scoring logic, regression harnesses, and evaluation run contracts.
- `scripts`: runnable developer workflows that compose services without owning business rules.
- `observability`: Prometheus scrape configuration, Grafana provisioning, dashboards, and future OpenTelemetry setup.

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

- Prefer one owner for one concept: OpenAlex normalization belongs in ingestion, citation-ready evidence belongs in retrieval, model calls belong in AI services, scoring belongs in evaluation, and metrics policy belongs in core/observability.
- Avoid duplicated business decisions across routes, scripts, and tests. If a rule affects behavior, put it in a service and test it there.
- Keep infrastructure concerns explicit: Docker, Kubernetes, Helm, Argo CD, Terraform, and CI/CD should be documented and implemented as real tools, not hidden behind generic wrappers.
- Do not introduce broad helper layers just to reduce a few repeated lines; add abstractions when they remove real coupling or repeated decisions.
- Keep public/private boundaries orthogonal to retrieval and AI behavior. Private learning material must stay outside public OpenAlex workflows.

## LangChain and LangGraph Ownership

LangChain is a framework dependency inside the retrieval and AI workflow path, not the owner of the application architecture.

LangChain owns:

- `Document` abstractions for retrieval-ready scholarly records
- retriever composition and retrieval pipeline primitives
- embedding interfaces and vector-store integrations
- future chain components that consume stable retrieval contracts

Project services own:

- OpenAlex normalization and refresh policy
- ranking policy, filters, evidence construction, and citation metadata
- API request/response contracts
- provenance, audit records, and database persistence
- evaluation scoring and observability policy

LangGraph owns workflow state and orchestration once Phase 3 begins. Its nodes should call retrieval, inference, evaluation, and observability services rather than reimplementing their behavior. LangGraph may coordinate retries, partial states, and failure transitions, but it should not own retrieval ranking, model provider details, or evaluation scoring.

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
- public-safe document chunks
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
- public-safe derived artifacts after ingestion and retrieval policy exists

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

The AI workflow strategy is evidence-first. Retrieval must produce structured evidence and citation metadata before answer generation.

LangChain should first appear through document mapping and retrievers. Raw provider calls may exist only behind small adapters for testing, mocking, or comparison, but they should not become the main application path.

Azure OpenAI is the first production inference provider. API routes and LangGraph nodes should call an inference service, not provider SDKs directly.

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
- expected-work hits
- citation coverage
- answer grounding
- unsupported-claim detection
- hallucination resistance
- privacy-boundary checks
- workflow regressions

Observability must cover:

- API request IDs
- ingestion runs
- retrieval latency and result counts
- Azure OpenAI calls, failures, and token usage
- LangChain call metadata where useful
- LangGraph node transitions
- retrieval traces
- latency and failures
- token and cost estimates when available
- evaluation run history
- Grafana dashboards for local inspection

Prometheus and Grafana are the first concrete observability stack. OpenTelemetry can be added after metrics and logs are stable. LangSmith may be added later as optional LangChain trace tooling, but default CI and local validation should not depend on paid or hosted tracing.

## Evolution Path

### Phase 0

Project foundation, specification system, LangChain-first architecture, logging, and private/public boundaries.

The Phase 0 Software Design Document is defined in `specs.md` and defines the foundation architecture, data model concepts, interface contracts, workflow expectations, and validation strategy.

### Phase 1

OpenAlex ingestion and database modeling.

Current Phase 1 status:

- the current ingestion slice is intentionally one-work-at-a-time for learning and traceability
- PostgreSQL is the primary database target
- ingestion persists audit and failure records as first-class tables
- retry execution exists at the service layer
- real ingestion, re-ingestion, Docker stack validation, PostgreSQL-backed tests, CI, and architecture ownership review are satisfied

### Phase 2

LangChain document mapping, retrieval contracts, metadata filters, citation-aware evidence, and `pgvector` semantic retrieval. Phase 2 begins with `Work -> LangChain Document` mapping before embeddings.

### Phase 3

LangGraph research workflow over retrieval, inference, evaluation, and observability services. LangGraph owns orchestration, not domain policy.

### Phase 4

Evaluation workflows and research quality controls for retrieval, citation coverage, groundedness, unsupported claims, privacy boundaries, and regressions.

### Phase 5

Production observability for API, ingestion, retrieval, Azure OpenAI calls, token usage, LangChain traces where useful, LangGraph workflows, eval runs, Prometheus metrics, and Grafana dashboards.

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
