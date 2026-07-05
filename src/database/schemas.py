"""
Pydantic models for validation and API contracts.

LEARNING NOTES ON PYDANTIC:

1. WHY PYDANTIC + SQLALCHEMY?
   - SQLAlchemy models define the database schema
   - Pydantic models define the API request/response contracts
   - Separation of concerns: DB models vs API schemas
   - Pydantic provides validation, type coercion, and serialization

2. PYDANTIC SCHEMA LAYERS:
   - Create (POST): what fields are required in the request?
   - Update (PATCH): what fields can be updated?
   - Read (GET): what fields are returned in response?
   - DB: maps to SQLAlchemy model

3. VALIDATION:
   - Automatic type coercion: str to int, etc.
   - Custom validators with @validator
   - Config.orm_mode = True allows reading from ORM objects
   - Optional[type] for nullable fields

4. EXAMPLE PATTERN:
   class WorkCreate(BaseModel):
       title: str  # required
       abstract: Optional[str] = None  # optional

   class WorkRead(BaseModel):
       id: int
       title: str
       class Config:
           orm_mode = True  # read from ORM model
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# INGESTION RUN SCHEMAS
# ==============================================================================

class IngestionRunCreate(ORMBaseModel):
    """
    LEARNING: Used when creating a new ingestion run.
    Only required fields are specified.
    """
    query_type: str
    query_params: Optional[dict] = None


class IngestionRunRead(ORMBaseModel):
    """
    LEARNING: Returned when fetching an ingestion run.
    
    Config.orm_mode = True allows Pydantic to read from SQLAlchemy objects.
    Without it, Pydantic expects a dict.
    """
    id: int
    query_type: str
    query_params: Optional[dict] = None
    record_count: int
    error_count: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str


class IngestionErrorRead(ORMBaseModel):
    """Structured record of a failed ingestion step."""
    id: int
    ingestion_run_id: int
    entity_type: str
    external_id: Optional[str] = None
    stage: str
    error_type: str
    retryable: bool
    error_message: str
    created_at: datetime
    
# ==============================================================================
# AUTHOR SCHEMAS
# ==============================================================================

class AuthorCreate(ORMBaseModel):
    """
    LEARNING: Minimal data to create an author from OpenAlex API.
    """
    openalex_id: str
    name: str
    display_name: Optional[str] = None
    orcid: Optional[str] = None


class AuthorUpdate(ORMBaseModel):
    """
    LEARNING: Fields that can be updated on an existing author.
    """
    h_index: Optional[int] = None
    citation_count: Optional[int] = None
    works_count: Optional[int] = None


class AuthorRead(ORMBaseModel):
    """
    LEARNING: Full author data returned in API responses.
    """
    id: int
    openalex_id: str
    name: str
    display_name: Optional[str] = None
    orcid: Optional[str] = None
    citation_count: int
    works_count: int
    h_index: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
# ==============================================================================
# TOPIC SCHEMAS
# ==============================================================================

class TopicCreate(ORMBaseModel):
    """Create a topic from OpenAlex data."""
    openalex_id: str
    name: str
    description: Optional[str] = None
    domain: Optional[str] = None
    level: Optional[int] = None
    keywords: Optional[List[str]] = None


class TopicRead(ORMBaseModel):
    """Full topic data returned in responses."""
    id: int
    openalex_id: str
    name: str
    description: Optional[str] = None
    domain: Optional[str] = None
    level: Optional[int] = None
    citation_count: int
    works_count: int
    keywords: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    
# ==============================================================================
# SOURCE SCHEMAS
# ==============================================================================

class SourceCreate(ORMBaseModel):
    """Create a source (journal, conference, publisher)."""
    openalex_id: str
    name: str
    source_type: Optional[str] = None
    issn: Optional[str] = None
    issn_l: Optional[str] = None
    publisher: Optional[str] = None
    country_code: Optional[str] = None
    homepage_url: Optional[str] = None
    is_open_access: bool = False


class SourceRead(ORMBaseModel):
    """Full source data."""
    id: int
    openalex_id: str
    name: str
    source_type: Optional[str] = None
    issn: Optional[str] = None
    publisher: Optional[str] = None
    is_open_access: bool
    created_at: datetime
    updated_at: datetime


class SourceReadMinimal(ORMBaseModel):
    """Minimal source info for nested work responses."""
    id: int
    openalex_id: str
    name: str
    
# ==============================================================================
# WORK SCHEMAS
# ==============================================================================

class WorkCreate(ORMBaseModel):
    """
    LEARNING: Minimal data to create a work.
    Used when ingesting from OpenAlex API.
    """
    openalex_id: str
    title: str
    abstract: Optional[str] = None
    doi: Optional[str] = None
    publish_date: Optional[datetime] = None
    publication_year: Optional[int] = None
    work_type: Optional[str] = None
    language: str = "en"
    open_access: bool = False
    citation_count: int = 0
    source_url: Optional[str] = None
    pdf_url: Optional[str] = None
    source_id: Optional[int] = None
    ingestion_run_id: Optional[int] = None
    raw_payload: Optional[dict] = None


class WorkUpdate(ORMBaseModel):
    """Fields that can be updated on existing work."""
    citation_count: Optional[int] = None
    open_access: Optional[bool] = None


class WorkReadMinimal(ORMBaseModel):
    """
    LEARNING: Minimal work data for list endpoints.
    Use this for performance (don't return full author/topic details).
    """
    id: int
    openalex_id: str
    title: str
    publication_year: Optional[int] = None
    open_access: bool
    citation_count: int
    source_id: Optional[int] = None
    created_at: datetime
    
class AuthorReadMinimal(ORMBaseModel):
    """Minimal author info for nested responses."""
    id: int
    openalex_id: str
    name: str
    
class TopicReadMinimal(ORMBaseModel):
    """Minimal topic info for nested responses."""
    id: int
    openalex_id: str
    name: str
    
class WorkReadFull(ORMBaseModel):
    """
    LEARNING: Full work data with related authors and topics.
    Use this for detail endpoints.
    
    PERFORMANCE NOTE:
    - Nested objects can cause N+1 query problems
    - Use relationship() and joinedload() in ORM to optimize
    - See queries.py for examples
    """
    id: int
    openalex_id: str
    title: str
    abstract: Optional[str] = None
    doi: Optional[str] = None
    publication_year: Optional[int] = None
    work_type: Optional[str] = None
    open_access: bool
    citation_count: int
    source_url: Optional[str] = None
    source: Optional[SourceReadMinimal] = None
    authors: List[AuthorReadMinimal] = []
    topics: List[TopicReadMinimal] = []
    created_at: datetime
    updated_at: datetime


class OpenAlexWorkIngestRequest(ORMBaseModel):
    """Request contract for ingesting one OpenAlex work."""
    openalex_id: str = Field(..., description="OpenAlex work identifier, e.g. W2741809807")


class IngestionResult(ORMBaseModel):
    """High-level result returned after one-work ingestion."""
    ingestion_run_id: int
    work_id: int
    work_openalex_id: str
    created: bool
    authors_synced: int
    topics_synced: int
    source_synced: bool


# ==============================================================================
# API FOUNDATION SCHEMAS
# ==============================================================================

class ErrorDetail(BaseModel):
    """Normalized API error body."""
    code: str
    detail: object
    request_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Top-level normalized API error response."""
    error: ErrorDetail


# ==============================================================================
# RETRIEVAL AND AI CONTRACT SCHEMAS
# ==============================================================================

class RetrievalRequest(BaseModel):
    """Request contract for evidence retrieval before generation."""
    question: str = Field(..., min_length=3)
    limit: int = Field(5, ge=1, le=20)
    publication_year_min: Optional[int] = None
    publication_year_max: Optional[int] = None
    require_open_access: bool = False


class CitationMetadata(BaseModel):
    """Citation fields returned with retrieved evidence."""
    openalex_id: str
    title: str
    doi: Optional[str] = None
    source_url: Optional[str] = None
    publication_year: Optional[int] = None


class EvidenceItem(BaseModel):
    """One retrieved scholarly evidence item."""
    work_id: int
    openalex_id: str
    title: str
    abstract: Optional[str] = None
    publication_year: Optional[int] = None
    citation_count: int
    source_name: Optional[str] = None
    citation: CitationMetadata


class RetrievalResponse(BaseModel):
    """Retrieval output used by later cited-answer generation."""
    question: str
    evidence: list[EvidenceItem]
    citations: list[CitationMetadata]
    grounding_status: str = "retrieval_only"
    
# ==============================================================================
# CITATION SCHEMAS
# ==============================================================================

class CitationCreate(ORMBaseModel):
    """Create a citation relationship."""
    source_work_id: int
    cited_work_id: int


class CitationRead(ORMBaseModel):
    """Citation relationship with work details."""
    id: int
    source_work_id: int
    cited_work_id: int
    
