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
- architecture ownership and module boundaries when the phase introduces new components

The implementation order should be:

1. phase goal and scope in `phases.md`
2. detailed requirements and validation in `specs.md`
3. executable tasks/checkpoints in `task.md`
4. implementation
5. validation evidence captured in `logs.md`

No phase should be treated as complete until its exit conditions and validation checks are satisfied.

## Architecture Quality Rules

All phase specs must preserve these design qualities:

- DRY by behavior: avoid duplicating business rules, provider policy, schema decisions, and deployment policy.
- Orthogonality: keep ingestion, retrieval, inference, evaluation, observability, persistence, API, and deployment as independently understandable modules.
- Explicit ownership: every new capability should have one clear home module or infrastructure folder.
- Thin API boundary: HTTP routes should validate/delegate/serialize, while services own application behavior.
- Contract separation: ORM models, Pydantic schemas, OpenAlex payloads, LangChain documents, evaluation cases, and Terraform/Kubernetes manifests should not collapse into one shared shape.
- Infrastructure transparency: Docker, Kubernetes, Helm, Argo CD, AWS, Terraform, Prometheus, and Grafana should remain visible learning artifacts rather than hidden behind custom wrappers.

Architecture checks should happen before closing each phase and should be recorded in `logs.md` when they produce decisions or follow-up tasks.

## 000 Project Foundation

Status: active

Goal:
Establish the repository operating system, LangChain-first architecture baseline, logging model, private-material exclusion policy, and project conventions.

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

- Purpose: create a production-grade scholarly research platform built around OpenAlex, with LangChain-based ingestion and retrieval, early LangGraph workflows, and a clear rule that private learning material stays outside tracked project artifacts.
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
- Define local-only material exclusion so private learning notes remain outside repository artifacts.

#### Non-functional Requirements

- The design must support testability through manual and automated checks.
- The foundation must support observability for API requests, ingestion runs, LangChain calls, workflow transitions, and evaluation history.
- The system must be designed to keep private learning material out of git.
- The architecture must be modular and extensible for later phases.
- The architecture must keep module ownership explicit and avoid duplicated business rules.
- The design must keep storage, API, retrieval, inference, evaluation, observability, and deployment concerns orthogonal.

#### Architecture and Component Boundaries

- Define the main components:
  - API/service layer
  - ingestion service
  - retrieval/search service
  - LangGraph workflow service
  - evaluation service
  - observability/logging service
- Define boundaries between public and private content.
- Define a LangChain-first path for AI workflows, with small adapters for raw provider access only when needed.
- Define where LangGraph enters the architecture: after retrieval has matured enough to support a meaningful research workflow.
- Define dependency direction so routes depend on services, services depend on database/core contracts, and infrastructure describes deployment without owning application behavior.
- Keep OpenAlex normalization, retrieval ranking, AI inference, evaluation scoring, and observability policy in separate owners.

#### Data Model and Storage Concepts

- Identify required entity types:
  - OpenAlex works, authors, sources, topics, citations
  - local documents and document chunks
  - embeddings and retrieval metadata
  - evaluation runs and workflow records
- Specify storage strategy:
  - PostgreSQL for structured metadata
  - `pgvector` for embeddings and semantic retrieval
  - local file storage for cached payloads
- Define provenance metadata for ingested records and local caches.

#### Interface and Contract Definitions

- Define contract expectations for:
  - OpenAlex ingestion adapters
  - LangChain document loaders / retrievers
  - LangGraph workflow states and transitions
  - API request/response shape for future workflows
- Capture contract-level requirements rather than full implementation signatures where appropriate.

#### Workflow Definitions

- Ingestion workflow: query OpenAlex, normalize entities, store structured records, cache raw payloads.
- Retrieval workflow: build LangChain-compatible retriever, support metadata filters, return evidence with citations.
- Research workflow: accept question, retrieve evidence, inspect sources, synthesize answer, validate grounding.
- Evaluation workflow: define metrics and test scenarios for retrieval quality and grounding.
- Observability workflow: capture request IDs, execution metadata, errors, and trace information.

#### Validation and Testing Plan

- Document manual test scripts for ingestion, retrieval, workflow execution, and observability.
- Document automated test areas for schema contracts, ingestion idempotency, retrieval filters, vector storage, workflow transitions, and evaluation metrics.
- Define success criteria for Phase 0 documentation and design readiness.

#### Public / Private Boundary and Git Exclusion

- The Phase 0 SDD must include explicit rules for excluded private learning material.
- Private learning material should stay outside tracked project artifacts.
- Public docs should summarize architectural choices and design intent without turning private notes into product scope.
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
- ingestion owns OpenAlex normalization and upsert behavior; API routes and scripts should call ingestion services rather than duplicate persistence rules
- SQL reference material must be kept aligned with Alembic and live PostgreSQL behavior

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

### Progressive CI/CD

CI/CD should be implemented gradually. Each project phase adds the checks that match the capability introduced in that phase.

The progression is:

1. Phase 1: lint, compile/import checks, PostgreSQL service, Alembic migration execution, and ingestion tests.
2. Phase 2: retrieval contract tests, filter/ranking tests, and vector-store checks.
3. Phase 3: mocked LangGraph workflow checks and state transition tests.
4. Phase 4: local evaluation smoke checks and stable regression thresholds.
5. Phase 5: metrics endpoint, structured log, and observability contract checks.
6. Phase 6: Kubernetes manifest and Helm template validation.
7. Phase 7: Argo CD Application manifest validation.
8. Phase 8: Terraform format, validate, and non-applying plan checks.
9. Phase 9: release promotion, environment approval, rollback, and deployment governance.

#### Delivery Order

For Phase 1 specifically, CI/CD should be introduced in two layers:

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
Establish the first continuous integration checkpoint from Phase 1. This is the start of CI/CD, not the entire final release system.

Includes:

- GitHub Actions workflow setup
- automated schema migration testing
- pytest integration
- linting and type checking (ruff, mypy)
- database initialization and cleanup
- environment configuration (.env.example)
- Docker containerization for consistency
- local development task automation
- early deployment pre-flight checks

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

#### CI/CD Growth Rule

Do not wait until a late phase to implement all automation. Add checks when the behavior exists and is worth enforcing. Phase 9 should consolidate and govern release promotion, not introduce basic CI for the first time.

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
- Retrieval owns evidence ranking and citation-ready response construction; AI synthesis should consume retrieval output rather than re-querying the database independently.

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
- Evaluation should depend on retrieval/workflow contracts and should not duplicate retrieval implementation details.

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
- Observability owns metrics/logging conventions; domain services may emit events or counters but should not grow custom metrics policy independently.

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

Architecture rule:

- Kubernetes and Helm describe deployment only. They must not redefine application configuration defaults that already belong in `.env.example`, settings, or documented environment contracts.

## 007 Argo CD GitOps

Status: planned

Goal:
Deploy the local Kubernetes stack through Argo CD so Git becomes the deployment source of truth.

Includes:

- local Argo CD installation
- Argo CD Application manifest
- Helm chart sync
- GitOps diff, sync, rollback, and drift inspection

Architecture rule:

- Argo CD owns GitOps sync behavior only. It should consume the Helm chart and environment values rather than duplicate Kubernetes manifests.

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

Architecture rule:

- Terraform owns cloud resources and IAM policy. Application behavior remains in the Python service and container image.

Out of default scope:

- EKS, because it is not close to free
- always-on managed PostgreSQL until cost and persistence requirements are explicit

## 009 CI/CD Release Gates and Promotion

Status: planned

Goal:
Consolidate the CI/CD checks built across earlier phases into a release promotion system with approval gates, rollback expectations, and cloud deployment governance.

Includes:

- CI workflow consolidation
- release promotion workflow
- environment approvals
- branch/tag rules
- cloud deployment approval
- rollback workflow documentation
- evidence that earlier checks still run before release

## 010 MCP Research Tools

Status: planned

Goal:
Expose selected research platform capabilities through MCP.

Includes:

- paper search
- work lookup
- cited summary generation
- research workflow execution
- evaluation run inspection

## 011 Production Hardening

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
