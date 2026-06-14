# Phase 1 Ingestion Policy

This file describes the current behavior of the single-work OpenAlex ingestion flow.

## Upsert rules

- OpenAlex is the source of truth for scholarly metadata stored in Phase 1 tables.
- `works` always refreshes the selected scholarly fields when a work payload is ingested.
- `authors`, `topics`, and `sources` refresh only the fields present in the payload used for that entity.
- Join tables (`works_authors`, `works_topics`) are replaced with the latest linkage for the ingested work.

## Recency rule

- "Prioritize newer publications" is a fetch-order decision for future batch ingestion.
- It does not change how one ingested work is persisted.
- Once a work payload is fetched, the upsert logic applies the same update rules regardless of publication year.

## Raw payload policy

- `works.raw_payload` stores the latest full work payload.
- Nested entities (`authors`, `topics`, `sources`) store the latest payload used to update them, even when that payload is partial.
- Phase 1 keeps only the latest payload, not a version history of payload snapshots.

## Partial source policy

- A nested OpenAlex source payload may be incomplete.
- The ingestion flow accepts partial source rows and updates only fields present in the payload.
- Missing keys do not clear previously known source metadata.

## Retry policy

- Retryable failures are transient infrastructure or network problems:
  - OpenAlex 5xx responses
  - connection drops
  - timeouts
  - temporary database connectivity problems
- Non-retryable failures are mapping or data-shape problems:
  - missing required identifiers
  - malformed payload structure
  - integrity problems caused by bad normalization logic
- `ingestion_errors.retryable` records this classification for later retry workflows.
