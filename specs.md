# Specs

## Spec Index

This file tracks the canonical features approved for implementation.

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

## 001 OpenAlex Ingestion Foundation

Status: planned

Goal:
Define how the system queries, stores, normalizes, and refreshes OpenAlex entities relevant to AI Reliability.

Includes:

- work ingestion
- author ingestion
- topic ingestion
- citation links
- local caching policy
- provenance metadata
- LangChain document mapping

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

## 005 Observability Foundation

Status: planned

Goal:
Track API requests, ingestion runs, LangChain call metadata, LangGraph execution records, retrieval traces, failures, latency, and evaluation history.

## 006 Private Notes Integration

Status: planned

Goal:
Allow local-only private notes to be indexed and used in personal research workflows without entering the public repository.

Includes:

- local-only notes ingestion
- private retrieval collection
- privacy guarantees
- git exclusion checks

## 007 MCP Research Tools

Status: planned

Goal:
Expose selected research platform capabilities through MCP.

Includes:

- paper search
- work lookup
- cited summary generation
- research workflow execution
- evaluation run inspection
