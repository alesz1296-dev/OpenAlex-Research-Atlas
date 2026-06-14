"""
SQLAlchemy ORM models for OpenAlex Research Atlas - Phase 1.

LEARNING NOTES ON SQLALCHEMY:

1. DECLARATIVE BASE:
   - Base is the parent class for all ORM models
   - Each model class = one database table
   - Columns defined with Column() type hints
   - Relationships defined with relationship()

2. COLUMN TYPES:
   - Integer, String, Text, Float, Boolean, DateTime, JSON, ARRAY, etc.
   - JSONB in PostgreSQL = JSON with indexing
   - nullable=False = NOT NULL constraint
   - default = default value or callable

3. RELATIONSHIPS:
   - One-to-many: use foreign key + relationship()
   - Many-to-many: use association table + relationship(secondary=)
   - Bidirectional: use back_populates on both sides

4. CONSTRAINTS:
   - primary_key=True
   - unique=True
   - UNIQUE() for multi-column unique constraint
   - ForeignKey() with ON DELETE CASCADE

5. QUERY PATTERNS (you'll use these):
   - db.query(Work).filter(Work.publication_year == 2024).all()
   - db.query(Work).join(Author).filter(Author.name == "Smith").all()
   - session.add(work_obj) -> session.commit()
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime,
    ForeignKey, UniqueConstraint, Index, JSON
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

# LEARNING: Create the base class for all ORM models
Base = declarative_base()


# ==============================================================================
# CORE OPENALEX ENTITIES
# ==============================================================================

class Work(Base):
    """
    LEARNING: Represents a scholarly work (article, paper, preprint).
    
    Table name: 'works'
    Relationships:
    - authors (many-to-many through works_authors)
    - topics (many-to-many through works_topics)
    - citations (work can cite many, and be cited by many)
    """
    __tablename__ = "works"
    
    # LEARNING: Primary Key
    id = Column(Integer, primary_key=True, index=True)  # surrogate key for efficiency
    
    # LEARNING: Natural Key (unique, stable identifier from OpenAlex)
    openalex_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Core metadata
    title = Column(Text, nullable=False)
    abstract = Column(Text, nullable=True)
    doi = Column(String(255), unique=True, nullable=True)
    
    # Dates
    publish_date = Column(DateTime, nullable=True)
    publication_year = Column(Integer, nullable=True, index=True)
    
    # Classification
    work_type = Column(String(50), nullable=True)  # article, preprint, book, etc.
    language = Column(String(10), default='en')
    
    # Metadata
    open_access = Column(Boolean, default=False)
    citation_count = Column(Integer, default=0)
    
    # URLs and storage
    source_url = Column(Text, nullable=True)
    pdf_url = Column(Text, nullable=True)
    source_id = Column(Integer, ForeignKey('sources.id', ondelete='SET NULL'), nullable=True)
    
    # Audit and provenance
    ingestion_run_id = Column(Integer, ForeignKey('ingestion_runs.id'), nullable=True)
    raw_payload = Column(JSONB, nullable=True)  # Full OpenAlex API response
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # LEARNING: Relationships (don't create columns, they're virtual)
    authors = relationship(
        "Author",
        secondary="works_authors",
        back_populates="works"
    )
    topics = relationship(
        "Topic",
        secondary="works_topics",
        back_populates="works"
    )
    source = relationship("Source", back_populates="works")
    cited_by = relationship(
        "Work",
        secondary="citations",
        primaryjoin="Work.id == citations.c.source_work_id",
        secondaryjoin="Work.id == citations.c.cited_work_id",
        foreign_keys="[citations.c.source_work_id, citations.c.cited_work_id]",
        backref="cites",
        viewonly=True
    )
    
    def __repr__(self):
        return f"<Work(id={self.id}, title={self.title[:50]}...)>"


class Author(Base):
    """
    LEARNING: Represents a scholar/contributor.
    
    Table name: 'authors'
    Relationships:
    - works (many-to-many through works_authors)
    """
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    openalex_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Name and identifiers
    name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=True)
    orcid = Column(String(50), nullable=True, unique=True)
    
    # Metadata
    citation_count = Column(Integer, default=0)
    works_count = Column(Integer, default=0)
    h_index = Column(Integer, nullable=True)
    
    # Provenance
    raw_payload = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    works = relationship(
        "Work",
        secondary="works_authors",
        back_populates="authors"
    )
    
    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"


class Topic(Base):
    """
    LEARNING: Represents a research topic/concept.
    
    Table name: 'topics'
    Relationships:
    - works (many-to-many through works_topics)
    """
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    openalex_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Topic metadata
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String(255), nullable=True)  # e.g., "computer-science"
    level = Column(Integer, nullable=True)  # hierarchical level
    
    # Metrics
    citation_count = Column(Integer, default=0)
    works_count = Column(Integer, default=0)
    
    # Keywords as array (PostgreSQL ARRAY type)
    keywords = Column(ARRAY(String), nullable=True)
    
    # Provenance
    raw_payload = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    works = relationship(
        "Work",
        secondary="works_topics",
        back_populates="topics"
    )
    
    def __repr__(self):
        return f"<Topic(id={self.id}, name={self.name})>"


class Source(Base):
    """
    LEARNING: Represents a journal, conference, or publisher.
    
    Table name: 'sources'
    """
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    openalex_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Publication metadata
    name = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=True)  # journal, conference, repository
    issn = Column(String(20), nullable=True)
    issn_l = Column(String(20), nullable=True)
    publisher = Column(String(255), nullable=True)
    country_code = Column(String(2), nullable=True)
    
    # URLs
    homepage_url = Column(Text, nullable=True)
    
    # Access metadata
    is_open_access = Column(Boolean, default=False)
    
    # Provenance
    raw_payload = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    works = relationship("Work", back_populates="source")
    
    def __repr__(self):
        return f"<Source(id={self.id}, name={self.name})>"


# ==============================================================================
# ASSOCIATION TABLES (Many-to-Many Relationships)
# ==============================================================================

class WorkAuthor(Base):
    """
    LEARNING: Association table for many-to-many work-author relationship.
    
    Why a separate table instead of just using secondary= in relationship()?
    - We need to store extra data: author_order (position in author list)
    - For complex many-to-many relationships, explicit association tables are clearer
    """
    __tablename__ = "works_authors"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    work_id = Column(Integer, ForeignKey('works.id', ondelete='CASCADE'), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Extra data: author position in the author list
    author_order = Column(Integer, nullable=False)  # 1 = first author, 2 = second, etc.
    
    # LEARNING: Unique constraint prevents duplicate work-author pairs
    __table_args__ = (
        UniqueConstraint('work_id', 'author_id', name='uq_work_author'),
    )


class WorkTopic(Base):
    """
    LEARNING: Association table for many-to-many work-topic relationship.
    
    Stores relevance score from OpenAlex.
    """
    __tablename__ = "works_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    work_id = Column(Integer, ForeignKey('works.id', ondelete='CASCADE'), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Extra data: relevance score
    score = Column(Float, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('work_id', 'topic_id', name='uq_work_topic'),
    )


class Citation(Base):
    """
    LEARNING: Represents a citation relationship between works.
    
    Directional: source_work_id -> cited_work_id means
    "source_work cites cited_work"
    """
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys (self-referencing: both point to works)
    source_work_id = Column(Integer, ForeignKey('works.id', ondelete='CASCADE'), nullable=False, index=True)
    cited_work_id = Column(Integer, ForeignKey('works.id', ondelete='CASCADE'), nullable=False, index=True)
    
    __table_args__ = (
        UniqueConstraint('source_work_id', 'cited_work_id', name='uq_citation'),
    )


# ==============================================================================
# OBSERVABILITY AND AUDIT TABLES
# ==============================================================================

class IngestionRun(Base):
    """
    LEARNING: Tracks each batch of OpenAlex ingestion.
    
    Used for:
    - Audit trail: which data was ingested when?
    - Replay: re-run a specific ingestion batch
    - Error tracking: which runs had failures?
    """
    __tablename__ = "ingestion_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # What was ingested?
    query_type = Column(String(50), nullable=False)  # 'works', 'authors', 'topics'
    query_params = Column(JSONB, nullable=True)  # Full OpenAlex query used
    
    # Results
    record_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default='running')  # running, completed, failed

    errors = relationship("IngestionError", back_populates="ingestion_run", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<IngestionRun(id={self.id}, query_type={self.query_type}, status={self.status})>"


class ApiLog(Base):
    """
    LEARNING: Structured logging for OpenAlex API calls.
    
    For observability:
    - Track response times
    - Monitor errors
    - Understand API behavior
    """
    __tablename__ = "api_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Request details
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, etc.
    
    # Response details
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=True)  # milliseconds
    error_message = Column(Text, nullable=True)
    
    # Linkage
    ingestion_run_id = Column(Integer, ForeignKey('ingestion_runs.id', ondelete='SET NULL'), nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)


class IngestionError(Base):
    """
    LEARNING: Records one failed ingestion attempt or sub-step.

    This table helps you answer:
    - what failed?
    - during which ingestion run?
    - for which external entity?
    - what payload caused the problem?
    """
    __tablename__ = "ingestion_errors"

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey('ingestion_runs.id', ondelete='CASCADE'), nullable=False, index=True)

    entity_type = Column(String(50), nullable=False)  # work, author, topic, source
    external_id = Column(String(255), nullable=True)  # OpenAlex identifier when available
    stage = Column(String(50), nullable=False)  # fetch, normalize, persist
    error_type = Column(String(100), nullable=False)
    retryable = Column(Boolean, default=False, nullable=False)
    error_message = Column(Text, nullable=False)
    raw_payload = Column(JSONB, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    ingestion_run = relationship("IngestionRun", back_populates="errors")
