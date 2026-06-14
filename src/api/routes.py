"""
API routes for OpenAlex Research Atlas.

LEARNING NOTES:

This is a stub for Phase 1. Real implementations come in later phases.

Routes follow RESTful patterns:
- GET /works -> list all works
- GET /works/{id} -> get one work
- POST /works -> create work (used by ingestion)
- PATCH /works/{id} -> update work
- GET /authors -> list authors
- etc.

For Phase 1, we focus on ingestion data loading, not API endpoints.
API routes will be built in Phase 2+ as needed.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.database import schemas
from src.database.models import Work, Author, Topic
from src.ingestion.openalex import OpenAlexIngestionService

router = APIRouter()


@router.get("/works", response_model=list[schemas.WorkReadMinimal])
def list_works(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    LEARNING: List works with pagination.
    
    Query parameters:
    - skip: offset for pagination (default 0)
    - limit: how many records (default 100, max 1000)
    
    Returns: list of WorkReadMinimal
    """
    works = db.query(Work).offset(skip).limit(limit).all()
    return works


@router.get("/works/{work_id}", response_model=schemas.WorkReadFull)
def get_work(work_id: int, db: Session = Depends(get_db)):
    """Get a single work by ID with full details."""
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    return work


@router.post("/works", response_model=schemas.WorkReadFull)
def create_work(work: schemas.WorkCreate, db: Session = Depends(get_db)):
    """
    LEARNING: Create a new work.
    
    This is used during ingestion to add OpenAlex works to the database.
    """
    db_work = Work(**work.model_dump())
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


@router.get("/authors", response_model=list[schemas.AuthorRead])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all authors."""
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors


@router.get("/topics", response_model=list[schemas.TopicRead])
def list_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all topics."""
    topics = db.query(Topic).offset(skip).limit(limit).all()
    return topics


@router.post("/ingestion/works", response_model=schemas.IngestionResult)
def ingest_one_work(request: schemas.OpenAlexWorkIngestRequest, db: Session = Depends(get_db)):
    """
    LEARNING: Ingest exactly one OpenAlex work.

    Why this endpoint exists:
    - it keeps the Phase 1 ingestion slice small
    - it is easier to debug one payload than a whole batch
    - once this works reliably, batching becomes a separate concern
    """
    service = OpenAlexIngestionService(db)
    result = service.ingest_work_by_openalex_id(request.openalex_id)
    return schemas.IngestionResult(**result.__dict__)
