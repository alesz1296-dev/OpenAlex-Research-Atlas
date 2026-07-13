# Phase 2 Retrieval Manual Runbook

This runbook is for learning and manually validating the first retrieval slice.

Current scope:

- keyword retrieval
- publication year filtering
- open-access filtering
- citation inspection

This runbook assumes Phase 1 ingestion is already working and the local Docker
stack is available.

## 1. Start the local stack

From the project root:

```powershell
docker compose up -d postgres api
```

If you want observability visible while testing:

```powershell
docker compose up -d prometheus grafana
```

## 2. Confirm the API is reachable

Check health:

```powershell
Invoke-WebRequest -UseBasicParsing http://localhost:8000/health
```

You should get an HTTP 200 response.

## 3. Make sure retrieval data exists

Ingest at least one or two real works first if your local database is empty:

```powershell
& 'C:\Users\alesz\AppData\Local\Programs\Python\Python311\python.exe' scripts/ingest_one_work.py W1234567890
```

Repeat with one or two additional OpenAlex work ids if you want a more useful
manual search set.

What to learn here:

- retrieval only works over persisted rows
- ingestion quality affects retrieval quality
- richer manual testing is easier once you have a few works with different years
  and open-access states

## 4. Keyword query

Run a keyword retrieval request:

```powershell
$body = @{
  question = "retrieval"
  limit = 5
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/retrieval/search `
  -ContentType "application/json" `
  -Body $body
```

What to verify:

- `retrieval_method` is `keyword`
- `result_count` matches the number of returned evidence items
- `evidence` contains titles, citation counts, matched fields, and citation data
- `citations` aligns with the evidence list

## 5. Year filter

Run a filtered query:

```powershell
$body = @{
  question = "retrieval"
  limit = 5
  publication_year_min = 2023
  publication_year_max = 2025
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/retrieval/search `
  -ContentType "application/json" `
  -Body $body
```

What to verify:

- `filters_applied.publication_year_min` and `publication_year_max` are present
- every returned evidence item is inside the requested year range
- no older work leaks into the results

## 6. Open-access filter

Run an open-access-only query:

```powershell
$body = @{
  question = "retrieval"
  limit = 5
  require_open_access = $true
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/retrieval/search `
  -ContentType "application/json" `
  -Body $body
```

What to verify:

- `filters_applied.require_open_access` is `true`
- only open-access works are returned
- result count may shrink compared with the unfiltered keyword query

## 7. Citation inspection

Inspect one returned evidence item carefully.

Check:

- `evidence[n].citation.openalex_id`
- `evidence[n].citation.title`
- `evidence[n].citation.doi`
- `evidence[n].citation.source_url`
- `evidence[n].citation.publication_year`

Then compare it with the top-level `citations` list.

What to verify:

- each evidence item has a citation object
- the top-level `citations` list is derived from the evidence items
- citation metadata is enough for later answer grounding and source tracing

## 8. Optional database cross-check

Open PostgreSQL:

```powershell
docker exec -it openalex-research-atlas-postgres psql -U openalex_user -d openalex_research
```

Then inspect rows:

```sql
SELECT id, openalex_id, title, publication_year, open_access, citation_count
FROM works
ORDER BY citation_count DESC, publication_year DESC;
```

What to learn here:

- retrieval ranking currently comes from database fields, not embeddings
- the manual API result should reflect the same ranking logic

## 9. What this runbook validates

This manual runbook validates the current Phase 2 retrieval baseline:

- request and response contract shape
- keyword retrieval path
- publication year filtering
- open-access filtering
- citation-ready evidence output

It does not yet validate:

- semantic retrieval
- embeddings
- `pgvector`
- LangGraph workflow behavior
- grounded answer generation from the full retrieval response
