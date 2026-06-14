# Architecture

## System Purpose

OpenAlex Research Atlas is a production-grade scholarly research intelligence platform that combines:

- public scholarly metadata from OpenAlex
- local enriched content such as abstracts, notes, and derived chunks
- private academic notes excluded from git
- LangChain workflows for retrieval, synthesis, comparison, and evaluation
- LangGraph workflows for stateful research processes

## Architectural Principles

- Spec-driven development before implementation.
- Clear separation between public project artifacts and private learning materials.
- Production-grade boundaries from the beginning: typed contracts, testability, logging, observability, and modular services.
- OpenAlex is the external source of truth for scholarly metadata.
- LangChain is part of the core architecture from the first implemented AI workflow.
- LangGraph is introduced early once retrieval can support a meaningful research workflow.
- Private notes may enrich local retrieval, but must remain isolated from public repo artifacts.

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
     -> Private Notes Indexer
  -> PostgreSQL + pgvector
  -> Local file storage for cached raw documents and private notes
```

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
- private notes
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
- private Markdown notes

## Boundary Between Public and Private

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
- private content exclusion

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

### Phase 2

LangChain retrieval and citation-aware academic search.

### Phase 3

LangGraph research workflow for grounded synthesis, comparison, and question answering.

### Phase 4

Evaluation workflows and research quality controls.

### Phase 5

Observability for API, ingestion, retrieval, LangChain calls, LangGraph workflows, and eval runs.

### Phase 6

Private notes integration with local-only indexing.

### Phase 7

MCP research tools.

### Phase 8

Deployment hardening and production operations.
