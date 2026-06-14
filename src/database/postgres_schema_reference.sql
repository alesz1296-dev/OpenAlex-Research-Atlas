CREATE TABLE ingestion_runs (
    id SERIAL PRIMARY KEY,
    query_type VARCHAR(50) NOT NULL,
    query_params JSONB,
    record_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    started_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(50) DEFAULT 'running'
);

CREATE INDEX ix_ingestion_runs_id ON ingestion_runs (id);

CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    openalex_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50),
    issn VARCHAR(20),
    issn_l VARCHAR(20),
    publisher VARCHAR(255),
    country_code VARCHAR(2),
    homepage_url TEXT,
    is_open_access BOOLEAN DEFAULT FALSE,
    raw_payload JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_sources_id ON sources (id);
CREATE UNIQUE INDEX ix_sources_openalex_id ON sources (openalex_id);

CREATE TABLE works (
    id SERIAL PRIMARY KEY,
    openalex_id VARCHAR(50) NOT NULL UNIQUE,
    title TEXT NOT NULL,
    abstract TEXT,
    doi VARCHAR(255) UNIQUE,
    publish_date TIMESTAMP WITHOUT TIME ZONE,
    publication_year INTEGER,
    work_type VARCHAR(50),
    language VARCHAR(10) DEFAULT 'en',
    open_access BOOLEAN DEFAULT FALSE,
    citation_count INTEGER DEFAULT 0,
    source_url TEXT,
    pdf_url TEXT,
    source_id INTEGER REFERENCES sources (id) ON DELETE SET NULL,
    ingestion_run_id INTEGER REFERENCES ingestion_runs (id),
    raw_payload JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_works_id ON works (id);
CREATE UNIQUE INDEX ix_works_openalex_id ON works (openalex_id);
CREATE INDEX ix_works_publication_year ON works (publication_year);

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    openalex_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    orcid VARCHAR(50) UNIQUE,
    citation_count INTEGER DEFAULT 0,
    works_count INTEGER DEFAULT 0,
    h_index INTEGER,
    raw_payload JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_authors_id ON authors (id);
CREATE UNIQUE INDEX ix_authors_openalex_id ON authors (openalex_id);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    openalex_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    domain VARCHAR(255),
    level INTEGER,
    citation_count INTEGER DEFAULT 0,
    works_count INTEGER DEFAULT 0,
    keywords VARCHAR[],
    raw_payload JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_topics_id ON topics (id);
CREATE UNIQUE INDEX ix_topics_openalex_id ON topics (openalex_id);

CREATE TABLE works_authors (
    id SERIAL PRIMARY KEY,
    work_id INTEGER NOT NULL REFERENCES works (id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors (id) ON DELETE CASCADE,
    author_order INTEGER NOT NULL,
    CONSTRAINT uq_work_author UNIQUE (work_id, author_id)
);

CREATE INDEX ix_works_authors_id ON works_authors (id);
CREATE INDEX ix_works_authors_work_id ON works_authors (work_id);
CREATE INDEX ix_works_authors_author_id ON works_authors (author_id);

CREATE TABLE works_topics (
    id SERIAL PRIMARY KEY,
    work_id INTEGER NOT NULL REFERENCES works (id) ON DELETE CASCADE,
    topic_id INTEGER NOT NULL REFERENCES topics (id) ON DELETE CASCADE,
    score DOUBLE PRECISION,
    CONSTRAINT uq_work_topic UNIQUE (work_id, topic_id)
);

CREATE INDEX ix_works_topics_id ON works_topics (id);
CREATE INDEX ix_works_topics_work_id ON works_topics (work_id);
CREATE INDEX ix_works_topics_topic_id ON works_topics (topic_id);

CREATE TABLE citations (
    id SERIAL PRIMARY KEY,
    source_work_id INTEGER NOT NULL REFERENCES works (id) ON DELETE CASCADE,
    cited_work_id INTEGER NOT NULL REFERENCES works (id) ON DELETE CASCADE,
    CONSTRAINT uq_citation UNIQUE (source_work_id, cited_work_id)
);

CREATE INDEX ix_citations_id ON citations (id);
CREATE INDEX ix_citations_source_work_id ON citations (source_work_id);
CREATE INDEX ix_citations_cited_work_id ON citations (cited_work_id);

CREATE TABLE api_logs (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    error_message TEXT,
    ingestion_run_id INTEGER REFERENCES ingestion_runs (id) ON DELETE SET NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_api_logs_id ON api_logs (id);

CREATE TABLE ingestion_errors (
    id SERIAL PRIMARY KEY,
    ingestion_run_id INTEGER NOT NULL REFERENCES ingestion_runs (id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL,
    external_id VARCHAR(255),
    stage VARCHAR(50) NOT NULL,
    error_type VARCHAR(100) NOT NULL,
    retryable BOOLEAN NOT NULL DEFAULT FALSE,
    error_message TEXT NOT NULL,
    raw_payload JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_ingestion_errors_id ON ingestion_errors (id);
CREATE INDEX ix_ingestion_errors_ingestion_run_id ON ingestion_errors (ingestion_run_id);
