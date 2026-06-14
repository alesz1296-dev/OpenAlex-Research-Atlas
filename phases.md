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

## Phase 1: LangChain OpenAlex Ingestion

Goal:
Use LangChain-compatible document abstractions while ingesting AI Reliability works from OpenAlex.

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
