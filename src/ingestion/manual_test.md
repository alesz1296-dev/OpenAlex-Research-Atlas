# Phase 1 Manual Learning Runbook

This runbook is for learning the current one-work ingestion flow end to end.

Session note:

- If you are resuming after a pause, start here.
- The goal of the next session is not new implementation first; it is manual validation and understanding of the Phase 1 system already built.

## 1. Start PostgreSQL with Docker

Make sure Docker Desktop is running first, then from the project root run:

```powershell
docker compose up -d postgres
```

This starts a local PostgreSQL instance with:

- database: `openalex_research`
- user: `openalex_user`
- password: `openalex_password`

For automated tests, start the separate disposable PostgreSQL test database:

```powershell
docker compose up -d postgres_test
```

This starts:

- database: `openalex_research_test`
- user: `openalex_user`
- password: `openalex_password`
- host port: `5433`

## 2. Create `.env.local`

Add a local environment file in the project root with:

```env
DATABASE_URL=postgresql://openalex_user:openalex_password@localhost:5432/openalex_research
TEST_DATABASE_URL=postgresql://openalex_user:openalex_password@localhost:5433/openalex_research_test
OPENALEX_MAILTO=your-email@example.com
```

`OPENALEX_MAILTO` is recommended when calling OpenAlex.

Keep `DATABASE_URL` and `TEST_DATABASE_URL` separate locally. The pytest fixture
uses Alembic `upgrade head` and `downgrade base`, so it should run against a
disposable test database, not your manual development database.

## 3. Apply migrations

Run:

```powershell
& 'C:\Users\alesz\AppData\Local\Programs\Python\Python311\python.exe' -m alembic upgrade head
```

What to learn here:

- Alembic applies revisions in order
- your database schema becomes the persisted form of the ORM design
- if a migration fails, the error usually points to a schema mismatch or connection issue

## 4. Ingest one work

Run:

```powershell
& 'C:\Users\alesz\AppData\Local\Programs\Python\Python311\python.exe' scripts/ingest_one_work.py W1234567890
```

Inside Docker, the same direct script form should now work too:

```powershell
docker compose run --rm api python scripts/ingest_one_work.py W1234567890
```

You can replace `W1234567890` with a real OpenAlex work id.

What to learn here:

- one ingestion run should create or update one `works` row
- related `sources`, `authors`, `topics`, and join rows should also appear
- `ingestion_runs` records the attempt
- nested `authors` and `topics` may be structurally correct but still sparse, because
  the work payload does not always include full enrichment fields for those entities

## 5. Re-run the same work

Run the same command again.

What to verify:

- the work is updated, not duplicated
- source, author, and topic rows are not duplicated
- join tables still match the latest OpenAlex payload

## 6. Inspect the rows in PostgreSQL

Open a PostgreSQL shell:

```powershell
docker exec -it openalex-research-atlas-postgres psql -U openalex_user -d openalex_research
```

Then inspect the tables:

```sql
SELECT id, query_type, record_count, error_count, status FROM ingestion_runs ORDER BY id;
SELECT id, openalex_id, title, publication_year, source_id FROM works;
SELECT id, openalex_id, name FROM sources;
SELECT id, openalex_id, name FROM authors;
SELECT id, work_id, author_id, author_order FROM works_authors ORDER BY work_id, author_order;
SELECT id, openalex_id, name FROM topics;
SELECT id, work_id, topic_id, score FROM works_topics;
SELECT id, stage, error_type, retryable, error_message FROM ingestion_errors ORDER BY id;
```

What to learn here:

- ORM relationships become ordinary foreign-key-linked tables
- join tables are the real storage for many-to-many links
- retryable vs non-retryable failures are stored as data, not just exceptions in memory

## 7. Run the first pytest learning tests

Run:

```powershell
$env:TEST_DATABASE_URL='postgresql://openalex_user:openalex_password@localhost:5433/openalex_research_test'
& 'C:\Users\alesz\AppData\Local\Programs\Python\Python311\python.exe' -m pytest tests/test_openalex_ingestion.py -q
```

What to learn here:

- tests use a PostgreSQL-backed fixture
- the first test proves upsert behavior
- the second test proves retryable failures can be retried through the service layer
