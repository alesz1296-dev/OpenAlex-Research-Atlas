# Specs

## Spec Index

This file tracks the canonical features approved for implementation.

## Spec-Driven Delivery Rules

Each phase spec should define, at minimum:

- goal
- in-scope capabilities
- implementation tasks or milestones
- exit conditions
- manual validation
- automated validation

The implementation order should be:

1. phase goal and scope in `phases.md`
2. detailed requirements and validation in `specs.md`
3. executable tasks/checkpoints in `task.md`
4. implementation
5. validation evidence captured in `logs.md`

No phase should be treated as complete until its exit conditions and validation checks are satisfied.

## 000 Project Foundation

Status: active

Goal:
Establish the repository operating system, LangChain-first architecture baseline, logging model, private-note boundary, and project conventions.

Includes:

- root project documents
- git and assistant working rules
- `.gitignore` for private material
- phase roadmap
- initial OpenAlex project thesis
- default production stack
- LangChain and LangGraph learning goals

### Phase 0 SDD Foundation

This section defines the Phase 0 Software Design Document for internal developer use. It captures the foundation design before implementation begins, with explicit system scope, architecture boundaries, data model intent, interface contracts, workflow expectations, and verification strategy.

#### System Overview

- Purpose: create a production-grade scholarly research platform built around OpenAlex, with LangChain-based ingestion and retrieval, early LangGraph workflows, and a strong boundary between public repo artifacts and local private notes.
- Scope:
  - define system intent and design principles
  - identify the first research domain slice: AI Reliability
  - establish the core architecture and stack choices
  - capture project-level non-functional requirements and validation goals
- Out of scope for Phase 0:
  - detailed ingestion implementation
  - concrete API production code
  - deployment automation beyond local development assumptions

#### Functional Requirements

- Define OpenAlex ingestion flow concepts, including work, author, topic, and citation metadata.
- Define LangChain-compatible document abstractions for scholarly records and local notes.
- Define retrieval behavior for search, filtering, citation-aware results, and semantic similarity.
- Define the first LangGraph research workflow shape: question, evidence retrieval, citation inspection, synthesis, grounding validation, and cited response.
- Define private note handling and the boundary between public and local-only data.

#### Non-functional Requirements

- The design must support testability through manual and automated checks.
- The foundation must support observability for API requests, ingestion runs, LangChain calls, workflow transitions, and evaluation history.
- The system must be designed to keep private notes out of git and prevent accidental public export.
- The architecture must be modular and extensible for later phases.

#### Architecture and Component Boundaries

- Define the main components:
  - API/service layer
  - ingestion service
  - retrieval/search service
  - LangGraph workflow service
  - evaluation service
  - observability/logging service
  - private note indexer
- Define boundaries between public and private content.
- Define a LangChain-first path for AI workflows, with small adapters for raw provider access only when needed.
- Define where LangGraph enters the architecture: after retrieval has matured enough to support a meaningful research workflow.

#### Data Model and Storage Concepts

- Identify required entity types:
  - OpenAlex works, authors, sources, topics, citations
  - local documents and document chunks
  - embeddings and retrieval metadata
  - evaluation runs and workflow records
- Specify storage strategy:
  - PostgreSQL for structured metadata
  - `pgvector` for embeddings and semantic retrieval
  - local file storage for cached payloads and private notes
- Define provenance metadata for ingested records and local caches.

#### Interface and Contract Definitions

- Define contract expectations for:
  - OpenAlex ingestion adapters
  - LangChain document loaders / retrievers
  - LangGraph workflow states and transitions
  - API request/response shape for future workflows
  - privacy gating for private note inclusion
- Capture contract-level requirements rather than full implementation signatures where appropriate.

#### Workflow Definitions

- Ingestion workflow: query OpenAlex, normalize entities, store structured records, cache raw payloads.
- Retrieval workflow: build LangChain-compatible retriever, support metadata filters, return evidence with citations.
- Research workflow: accept question, retrieve evidence, inspect sources, synthesize answer, validate grounding.
- Evaluation workflow: define metrics and test scenarios for retrieval quality, grounding, and private note exclusion.
- Observability workflow: capture request IDs, execution metadata, errors, and trace information.

#### Validation and Testing Plan

- Document manual test scripts for ingestion, retrieval, workflow execution, private note exclusion, and observability.
- Document automated test areas for schema contracts, ingestion idempotency, retrieval filters, vector storage, workflow transitions, and evaluation metrics.
- Define success criteria for Phase 0 documentation and design readiness.

#### Public / Private Boundary and Git Exclusion

- The Phase 0 SDD must include explicit rules for private notes and excluded content.
- Private notes should be kept inside `private/` and excluded from git.
- Public docs should summarize architectural choices and design intent without exposing private learning materials.
- `.gitignore` rules must be validated as part of Phase 0.

#### Verification

- Confirm `specs.md` contains the Phase 0 SDD section with all subsections.
- Confirm the design section references existing root docs and preserves the repo’s foundation principles.
- Confirm `task.md` includes a Phase 0 SDD task for documentation and verification.

## 001 OpenAlex Ingestion Foundation

Status: planned

Goal:
Define how the system queries, stores, normalizes, and refreshes OpenAlex entities relevant to AI Reliability. Includes data model design, SQL schema, and SQLAlchemy ORM mapping.

Includes:

- work ingestion
- author ingestion
- topic ingestion
- citation links
- local caching policy
- provenance metadata
- LangChain document mapping
- Phase 1 data model and SQL schema design
- SQLAlchemy ORM models for OpenAlex entities
- timestamps and audit metadata

### Phase 1 Data Model Design

#### Core Entities (OpenAlex Focus)

- **works**: scholarly articles, papers, preprints (OpenAlex work entity)
- **authors**: scholars and contributors (OpenAlex author entity)
- **topics**: research areas and concepts (OpenAlex topic entity)
- **sources**: journals, conferences, publishers (OpenAlex source entity)
- **citations**: work-to-work citation relationships
- **works_authors**: junction table for many-to-many work-author relationships
- **works_topics**: junction table for many-to-many work-topic relationships

#### Observability and Audit Entities

- **ingestion_runs**: track OpenAlex API queries and ingestion batches
- **api_logs**: structured logs for API requests, errors, and performance
- **ingestion_errors**: failed ingestion records for retry logic

#### Metadata and Timestamps

All entities include:

- `created_at`: record creation timestamp
- `updated_at`: last modification timestamp
- `source_id`: identifier from OpenAlex API (to avoid duplicates)
- `raw_payload`: optional JSON cache of original API response

#### Phase 1 Scope

Phase 1 focuses on OpenAlex entities only. Local documents, chunks, embeddings, and evaluation records are deferred to Phase 2+.

Current implementation checkpoint:

- the first implementation slice uses one-work ingestion rather than paginated batch ingestion
- PostgreSQL remains the primary execution target for both development and testing
- retry classification and retry execution entry points exist, but full retry orchestration is deferred until manual validation is complete

### SQL Schema Design (Learning Exercise)

You will:

1. Design the SQL schema for Phase 1 entities (works, authors, topics, sources, citations).
2. Define relationships and constraints.
3. Plan indexes for ingestion and future retrieval queries.
4. Then implement as SQLAlchemy ORM models.

### SQLAlchemy ORM Mapping

After schema design, you will:

1. Create Pydantic models for validation and contracts.
2. Define SQLAlchemy declarative models with relationships.
3. Learn about session management and query patterns.

### CI/CD for Phase 1

From the start, plan:

1. Schema migrations using Alembic.
2. Local testing with pytest in the same PostgreSQL-oriented environment used by development.
3. Database reset scripts for development.
4. Schema versioning and rollback strategy.

#### Delivery Order

For this project, CI/CD should be introduced in two layers:

1. **Docker first in Phase 1**:
   - containerize PostgreSQL and the application runtime for consistent local development
   - use Docker Compose or an equivalent local orchestration setup
   - make migrations and one-work ingestion runnable inside the same environment the tests will use later
2. **CI second once ingestion is testable**:
   - add GitHub Actions only after the repository has
     - working Dockerized local development,
     - applied Alembic migrations,
     - at least one ingestion-focused automated test,
     - basic lint / import verification worth enforcing in pull requests

This order keeps CI meaningful. The pipeline should validate real project behavior, not just an empty scaffold.

## 001.1 CI/CD Pipeline Foundation

Status: planned

Goal:
Establish continuous integration and deployment practices from Phase 1. Includes local development automation, testing, and deployment readiness.

Includes:

- GitHub Actions workflow setup
- automated schema migration testing
- pytest integration
- linting and type checking (ruff, mypy)
- database initialization and cleanup
- environment configuration (.env.example)
- Docker containerization for consistency
- local development task automation
- deployment pre-flight checks

#### Phase 1 CI/CD Scope

- Local development: Dockerized PostgreSQL, pytest, linting, type checks
- Schema migration testing with Alembic
- Environment management (.env, .env.local exclusion)
- GitHub Actions workflow for PR validation after the first ingestion tests exist
- Database setup and reset automation

#### CI/CD Learning Goals

You will:

1. Understand pytest fixtures for database isolation
2. Learn Alembic for schema versioning
3. Practice environment management and secrets handling
4. Build reusable GitHub Actions workflows

## 002 LangChain Retrieval

Status: planned

Goal:
Provide keyword, filtered, citation-aware, and semantic retrieval across ingested scholarly records and approved local materials using LangChain-compatible abstractions.

Includes:

- embeddings
- `pgvector`
- LangChain retrievers
- metadata filters
- citation-aware document retrieval

Initial implementation notes:

- `POST /retrieval/search` exists as the first retrieval API contract.
- The request accepts question, limit, optional publication-year bounds, and optional open-access filtering.
- The response separates question, evidence, citations, and grounding_status.
- The first retrieval implementation is keyword/filter retrieval over ingested OpenAlex works.
- Semantic retrieval with `pgvector` remains the next Phase 2 expansion.

## 003 LangGraph Research Workflow

Status: planned

Goal:
Create the first stateful research workflow with LangGraph.

Includes:

- research question input
- evidence retrieval
- citation inspection
- grounded synthesis
- grounding validation
- cited response output

## 004 Evaluation and Quality Controls

Status: planned

Goal:
Measure retrieval quality, answer grounding, hallucination resistance, private content exclusion, and workflow regressions.

Includes:

- manual test scripts
- automated evaluation fixtures
- retrieval metrics
- answer-grounding checks
- regression tracking

Initial implementation notes:

- A local retrieval evaluation harness exists.
- A seed eval dataset exists under `evals/`.
- Default evaluation does not make Azure OpenAI calls.
- Future expansion should add grounding and privacy-boundary datasets after cited-answer generation exists.

## 005 Observability Foundation

Status: planned

Goal:
Track API requests, ingestion runs, LangChain call metadata, LangGraph execution records, retrieval traces, failures, latency, and evaluation history.

Initial implementation notes:

- `/metrics` exposes Prometheus metrics from the API.
- Request count and latency are tracked by method, route, and status code.
- Retrieval, Azure OpenAI, and evaluation counters exist.
- Grafana is provisioned locally through Docker Compose.
- Structured JSON logs include request IDs for API requests.

## 006 Local Kubernetes and Helm

Status: planned

Goal:
Run the platform locally on Kubernetes and package it with Helm while keeping the real Kubernetes objects visible for learning.

Includes:

- `kind` local cluster
- raw Kubernetes manifests before Helm packaging
- API Deployment and Service
- PostgreSQL local Kubernetes deployment for learning
- ConfigMaps and Secrets
- Alembic migration Job
- health and readiness probes
- Helm chart, values, install, upgrade, rollback, and uninstall workflow

## 007 Argo CD GitOps

Status: planned

Goal:
Deploy the local Kubernetes stack through Argo CD so Git becomes the deployment source of truth.

Includes:

- local Argo CD installation
- Argo CD Application manifest
- Helm chart sync
- GitOps diff, sync, rollback, and drift inspection

## 008 AWS Terraform Low-Cost Deployment

Status: planned

Goal:
Deploy the API to AWS through Terraform while keeping the default path close to free or low-cost.

Includes:

- ECR
- GitHub Actions OIDC to AWS
- Lambda container image plus API Gateway as the default runtime
- CloudWatch logs
- Terraform modules and environment values
- smoke tests
- teardown and cost guardrails
- optional later ECS Fargate learning track

Out of default scope:

- EKS, because it is not close to free
- always-on managed PostgreSQL until cost and persistence requirements are explicit

## 009 CI/CD and Release Gates

Status: planned

Goal:
Make local validation, Docker builds, Kubernetes checks, Helm checks, and Terraform checks repeatable in CI/CD.

Includes:

- GitHub Actions lint/test workflow
- PostgreSQL-backed migration/test workflow
- Docker image build validation
- Helm template validation
- Terraform format, validate, and plan checks
- manual approval before cloud apply

## 010 Private Notes Integration

Status: planned

Goal:
Allow local-only private notes to be indexed and used in personal research workflows without entering the public repository.

Includes:

- local-only notes ingestion
- private retrieval collection
- privacy guarantees
- git exclusion checks

## 011 MCP Research Tools

Status: planned

Goal:
Expose selected research platform capabilities through MCP.

Includes:

- paper search
- work lookup
- cited summary generation
- research workflow execution
- evaluation run inspection

## 012 Production Hardening

Status: planned

Goal:
Harden the platform after the local Kubernetes, GitOps, CI/CD, and AWS Terraform paths exist.

Includes:

- authentication and authorization
- secret handling
- deployment rollback procedures
- operational runbooks
- observability review
- production smoke tests
- incident and recovery documentation
