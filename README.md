# OpenAlex Research Atlas

OpenAlex Research Atlas is a spec-driven, production-grade scholarly research platform built around OpenAlex as the primary reference database.

The system is intended to evolve from a local research platform into a deployed AI application. It will support ingestion of scholarly metadata, LangChain-based retrieval, LangGraph research workflows, citation-aware question answering, topic exploration, private annotations, evaluation workflows, and observability.

## Project Intent

- Use OpenAlex as the external scholarly knowledge backbone.
- Use LangChain from the first implemented AI and retrieval workflows.
- Introduce LangGraph early for stateful research workflows.
- Build the project through specification-driven development.
- Keep academic notes, reflections, and private references local and out of git.
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

Private notes live under `private/` and are intentionally excluded from git. They can contain:

- reading notes
- paper summaries
- prompt experiments
- architecture reflections
- weekly learning logs

## Initial Thesis

This project builds a production-grade OpenAlex research platform while privately supporting deep learning of LangChain, LangGraph, MCP, RAG, evaluation, and AI observability.

The public repository should present the system as a serious scholarly research platform. Private local notes may document the academic learning process in more detail.
