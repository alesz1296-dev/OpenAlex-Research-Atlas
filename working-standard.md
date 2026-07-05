# Working Standard

## Default Development Mode

This project uses specification-driven development. Work starts with documentation and contracts, then moves into implementation.

Before any meaningful implementation:

- confirm the feature exists in `specs.md`
- define or refine work in `task.md`
- ensure the architecture impact is reflected in `architecture.md`
- record notable session progress in `logs.md`

## Spec-Driven Development Workflow

Every phase should move through the same operating sequence:

1. Define the phase goal and scope in `phases.md`.
2. Record the canonical requirements, interfaces, and validation expectations in `specs.md`.
3. Break implementation into concrete tasks and checkpoints in `task.md`.
4. Implement only after the phase or stage has clear exit conditions.
5. Validate the phase using the documented manual and automated checks.
6. Record what was completed, what is pending, and any validation results in `logs.md`.

For each phase or stage, the docs should answer:

- what problem the phase solves
- what is in scope and out of scope
- what must exist before implementation starts
- what artifacts or code must be produced
- what conditions must be true to exit the phase
- how the phase is validated manually and automatically

Implementation should not outrun the written spec for long. If a design decision changes the intended behavior, update the Markdown source of truth in the same working session.

## LangChain and LangGraph Learning Standard

LangChain is part of the implementation path from the first AI and retrieval workflows.

LangGraph should be introduced early for stateful research workflows once retrieval can provide useful evidence.

Private local material may document framework learning, mistakes, comparisons, and reflections. Public docs should describe architectural choices and production behavior without turning private notes into product scope.

## Markdown as Project Memory

Project Markdown files are the primary context recovery mechanism for this repository.

Assistants and contributors should:

- read the root Markdown files before starting work
- use them to recover project context between sessions
- update them when the project changes materially
- avoid letting code diverge from documented intent for long periods

## Prompt Completion Summary

Every work update or task summary should explicitly include:

- what was completed,
- what is pending for the current phase,
- an overview of the changes made.

This summary style should be reflected in project documentation, issue updates, and assistant responses to keep progress clear and traceable.

## Change Discipline

- prefer small, reviewable increments
- keep tasks scoped to one logical outcome
- document assumptions explicitly
- preserve the boundary between public repo artifacts and private local notes
- define exit criteria before calling a phase or stage complete
- keep validation criteria visible in the phase and task docs, not only in chat

## Architecture Discipline

Every implementation pass should preserve modularity, orthogonality, and clear ownership.

Before adding or changing code, check:

- which module owns the behavior
- whether the change duplicates a business rule already implemented elsewhere
- whether the API layer is staying thin
- whether service modules remain independent of HTTP framework details
- whether persistence models, API schemas, and external provider payloads remain separate contracts
- whether cross-cutting concerns such as config, logging, metrics, and secrets stay in `src/core` or infrastructure-specific folders

DRY rule:

- Extract repeated business rules or repeated infrastructure policy.
- Do not extract merely because two pieces of code look similar.
- Keep separate models when they serve separate boundaries, such as ORM tables and Pydantic response contracts.

Orthogonality rule:

- Ingestion should not own retrieval behavior.
- Retrieval should not own inference behavior.
- AI provider adapters should not own API routing or database session lifecycle.
- Evaluation should depend on stable service contracts, not hidden implementation details.
- Deployment tooling should describe and run the platform, not redefine application behavior.

## Private Material Policy

- Private material is local-only working context.
- Private material may inform implementation and research direction.
- Private material must not be committed.
- Private material is not a product feature, retrieval source, implementation phase, or public documentation deliverable.
- Public docs should summarize conclusions without copying private note content.

## Production-Grade Expectations

Even in early phases, design for:

- typed schemas
- modular services
- explicit module ownership
- DRY business rules
- orthogonal concerns
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
- private material exclusion from git

Automated testing should verify:

- fixture parsing
- schema contracts
- ingestion idempotency
- retrieval filters
- vector storage contracts
- LangGraph state transitions
- evaluation metric calculations
- private path exclusion
