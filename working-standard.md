# Working Standard

## Default Development Mode

This project uses specification-driven development. Work starts with documentation and contracts, then moves into implementation.

Before any meaningful implementation:

- confirm the feature exists in `specs.md`
- define or refine work in `task.md`
- ensure the architecture impact is reflected in `architecture.md`
- record notable session progress in `logs.md`

## LangChain and LangGraph Learning Standard

LangChain is part of the implementation path from the first AI and retrieval workflows.

LangGraph should be introduced early for stateful research workflows once retrieval can provide useful evidence.

Private notes may document framework learning, mistakes, comparisons, and reflections. Public docs should describe architectural choices and production behavior without exposing private learning material.

## Markdown as Project Memory

Project Markdown files are the primary context recovery mechanism for this repository.

Assistants and contributors should:

- read the root Markdown files before starting work
- use them to recover project context between sessions
- update them when the project changes materially
- avoid letting code diverge from documented intent for long periods

## Change Discipline

- prefer small, reviewable increments
- keep tasks scoped to one logical outcome
- document assumptions explicitly
- preserve the boundary between public repo artifacts and private local notes

## Private Notes Policy

- Private notes are local-only working context.
- Private notes may inform implementation and research direction.
- Private notes must not be committed.
- Public docs should summarize conclusions without copying private note content.

## Production-Grade Expectations

Even in early phases, design for:

- typed schemas
- modular services
- testability
- structured logging
- config separation
- data provenance
- observability
- secure handling of secrets and private content

## Testing Standard

Use manual and automated testing together.

Manual testing should verify:

- OpenAlex ingestion behavior
- retrieval quality
- cited answer quality
- LangGraph workflow behavior
- observability records
- private-note exclusion

Automated testing should verify:

- fixture parsing
- schema contracts
- ingestion idempotency
- retrieval filters
- vector storage contracts
- LangGraph state transitions
- evaluation metric calculations
- private path exclusion
