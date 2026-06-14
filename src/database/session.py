"""
Database session management and connection pooling.

LEARNING NOTES:
- SessionLocal creates a new database session for each request
- engine manages the connection pool
- get_db() is a dependency for FastAPI routes
- Session lifecycle: create -> use -> commit/rollback -> close
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings


# LEARNING: create_engine creates a connection pool
# pool_size = max persistent connections
# max_overflow = extra connections allowed temporarily
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,  # SQL query logging
    pool_size=10,
    max_overflow=20,
)

# LEARNING: sessionmaker is a factory that creates Session objects
# Each Session is tied to one database transaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency for FastAPI routes to get a database session.
    
    LEARNING:
    - This is a generator function (uses 'yield')
    - FastAPI runs code before 'yield' for setup
    - Code after 'yield' runs for cleanup (always executes, even on error)
    - Very similar to try/finally pattern
    
    Usage in FastAPI:
        @app.get("/works")
        def get_works(db: Session = Depends(get_db)):
            return db.query(Work).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
